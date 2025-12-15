from fastapi import HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import case
from sqlalchemy.orm import Session

from app.core.book import book_core
from app.enums import CommentRejectionReason, CommentStatus, CommentStatusInput
from app.helpers.error_helper import Error
from app.models import AdminUser, BookComment, User
from app.schemas.panel.comment import CommentIn


class CommentCore:
    # User methods
    def create_comment(self, db: Session, book_id: int, user: User, data: CommentIn):
        book_core.get_book_by_id(db=db, book_id=book_id, only_active=False)

        exists = (
            db.query(BookComment.id)
            .filter(
                BookComment.book_id == book_id,
                BookComment.user_id == user.id,
                BookComment.status != CommentStatus.deleted,
            )
            .first()
        )
        if exists:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=Error.comment_already_exists)

        comment = BookComment(
            book_id=book_id,
            user_id=user.id,
            rating=data.rating,
            comment=data.comment,
            is_visible=data.is_visible,
            status=CommentStatus.pending,
        )
        db.add(comment)
        db.commit()
        return comment

    def get_user_comments(self, db: Session, user: User):
        masked_rating = case(
            (BookComment.status == CommentStatus.rejected, None),
            else_=BookComment.rating,
        )
        masked_comment = case(
            (BookComment.status == CommentStatus.rejected, None),
            else_=BookComment.comment,
        )

        return paginate(
            db.query(
                BookComment.id.label("id"),
                BookComment.date_created.label("date_created"),
                BookComment.book_id.label("book_id"),
                BookComment.status.label("status"),
                BookComment.is_visible.label("is_visible"),
                BookComment.rejection_reason.label("rejection_reason"),
                masked_rating.label("rating"),
                masked_comment.label("comment"),
            )
            .filter(
                BookComment.user_id == user.id,
                BookComment.status != CommentStatus.deleted,
            )
            .order_by(BookComment.date_created.desc())
        )

    def get_user_comment_detail(self, db: Session, user: User, comment_id: int):
        masked_rating = case(
            (BookComment.status == CommentStatus.rejected, None),
            else_=BookComment.rating,
        )
        masked_comment = case(
            (BookComment.status == CommentStatus.rejected, None),
            else_=BookComment.comment,
        )

        filters = [
            BookComment.id == comment_id,
            BookComment.user_id == user.id,
            BookComment.status != CommentStatus.deleted,
        ]

        query = (
            db.query(BookComment)
            .filter(*filters)
            .with_entities(
                BookComment.id.label("id"),
                BookComment.date_created.label("date_created"),
                BookComment.book_id.label("book_id"),
                BookComment.status.label("status"),
                BookComment.is_visible.label("is_visible"),
                BookComment.rejection_reason.label("rejection_reason"),
                masked_rating.label("rating"),
                masked_comment.label("comment"),
            )
        )

        row = query.first()
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=Error.comment_not_found)

        return row

    def delete_user_comment(self, db: Session, user: User, comment_id: int):
        comment = (
            db.query(BookComment)
            .filter(
                BookComment.id == comment_id,
                BookComment.user_id == user.id,
                BookComment.status != CommentStatus.deleted,
            )
            .first()
        )
        if not comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=Error.comment_not_found)

        comment.status = CommentStatus.deleted
        db.commit()
        return {"message": "Comment deleted."}

    # Admin methods
    def get_admin_comments(self, db: Session, status: CommentStatus | None = None):
        query = (
            db.query(
                BookComment.id.label("id"),
                BookComment.date_created.label("date_created"),
                BookComment.book_id.label("book_id"),
                User.id.label("user_id"),
                User.full_name.label("user_name"),
                BookComment.rating.label("rating"),
                BookComment.status.label("status"),
            )
            .join(User, User.id == BookComment.user_id)
            .filter(BookComment.status != CommentStatus.deleted)
            .order_by(BookComment.date_created.desc())
        )

        if status is not None:
            query = query.filter(BookComment.status == status)

        return paginate(query)

    def get_admin_comment_detail(self, db: Session, comment_id: int):
        filters = [
            BookComment.id == comment_id,
            BookComment.status != CommentStatus.deleted,
        ]

        query = (
            db.query(BookComment)
            .join(User, User.id == BookComment.user_id)
            .filter(*filters)
            .with_entities(
                BookComment.id.label("id"),
                BookComment.date_created.label("date_created"),
                BookComment.book_id.label("book_id"),
                User.id.label("user_id"),
                User.full_name.label("user_name"),
                BookComment.rating.label("rating"),
                BookComment.comment.label("comment"),
                BookComment.is_visible.label("is_visible"),
                BookComment.status.label("status"),
                BookComment.rejection_reason.label("rejection_reason"),
                BookComment.submitted_by_id.label("submitted_by_id"),
            )
        )

        row = query.first()
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=Error.comment_not_found)

        return row

    def admin_set_status(
        self,
        db: Session,
        comment_id: int,
        admin_user: AdminUser,
        new_status: CommentStatusInput,
        reason_enum: CommentRejectionReason | None,
        reason_text: str | None,
    ) -> None:
        comment = (
            db.query(BookComment)
            .filter(BookComment.id == comment_id, BookComment.status != CommentStatus.deleted)
            .first()
        )
        if not comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=Error.comment_not_found)

        if new_status == CommentStatusInput.rejected:
            if not reason_enum and not reason_text:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=Error.rejection_reason_required)

            parts: list[str] = []
            if reason_enum:
                parts.append(reason_enum.value)
            if reason_text:
                parts.append(reason_text)

            comment.status = CommentStatus.rejected
            comment.rejection_reason = " | ".join(parts)
        else:
            comment.status = CommentStatus.approved
            comment.rejection_reason = None

        comment.submitted_by_id = admin_user.id
        db.commit()


comment_core = CommentCore()
