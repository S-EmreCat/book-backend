from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.comment import comment_core
from app.enums import CommentStatus
from app.models import AdminUser
from app.schemas.admin.comment import CommentListOut, CommentOut, CommentStatusIn
from app.schemas.pagination import CustomPage
from app.views.admin.deps import get_current_admin_user
from app.views.deps import get_db

router = APIRouter()


@router.get("", response_model=CustomPage[CommentListOut], summary="Yorumları listele")
def list_comments(
    status: CommentStatus | None = None,
    db: Session = Depends(get_db),
):
    return comment_core.get_admin_comments(db=db, status=status)


@router.get("/{comment_id}", response_model=CommentOut, summary="Yorum detayı")
def get_comment_detail(
    comment_id: int,
    db: Session = Depends(get_db),
):
    return comment_core.get_admin_comment_detail(db=db, comment_id=comment_id)


@router.post("/{comment_id}/status", summary="Yorumu onayla / reddet")
def set_comment_status(
    comment_id: int,
    data: CommentStatusIn,
    db: Session = Depends(get_db),
    admin_user: AdminUser = Depends(get_current_admin_user),
):
    comment_core.admin_set_status(
        db=db,
        comment_id=comment_id,
        admin_user=admin_user,
        new_status=data.status,
        reason_enum=data.reason_enum,
        reason_text=data.reason_text,
    )
    return {"message": "Status updated."}


@router.post("/{comment_id}/confirm", summary="Yorumu hızlı onayla")
def confirm_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    admin_user: AdminUser = Depends(get_current_admin_user),
):
    comment_core.admin_set_status(
        db=db,
        comment_id=comment_id,
        admin_user=admin_user,
        new_status=CommentStatus.approved,
        reason_enum=None,
        reason_text=None,
    )
    return {"message": "Comment approved."}
