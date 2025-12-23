from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.comment import comment_core
from app.core.user import user_core
from app.models.user import User
from app.schemas.pagination import CustomPage
from app.schemas.panel.comment import CommentListOut
from app.schemas.panel.user import UserDetailOut, UserMeUpdateIn
from app.views.deps import get_db
from app.views.panel.deps import get_current_panel_user

router = APIRouter()


@router.get("/me", response_model=UserDetailOut, summary="Profilimi Görüntüle")
def get_me(
    panel_user: User = Depends(get_current_panel_user),
):
    return panel_user


@router.put("/me", response_model=UserMeUpdateIn, summary="Profilimi Güncelle")
def update_me(
    data: UserMeUpdateIn,
    db: Session = Depends(get_db),
    panel_user: User = Depends(get_current_panel_user),
):
    return user_core.update_me(db=db, user=panel_user, data=data)


@router.get("/comments", response_model=CustomPage[CommentListOut], summary="Kullanıcının yorumları")
def get_user_comments(
    db: Session = Depends(get_db),
    panel_user: User = Depends(get_current_panel_user),
):
    return comment_core.get_user_comments(db=db, user=panel_user)


@router.get("/comments/{comment_id}", response_model=CommentListOut, summary="Kullanıcı yorum detayı")
def get_my_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    panel_user: User = Depends(get_current_panel_user),
):
    return comment_core.get_user_comment_detail(db=db, user=panel_user, comment_id=comment_id)


@router.delete("/comments/{comment_id}", summary="Kullanıcı yorum sil")
def delete_my_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    panel_user: User = Depends(get_current_panel_user),
):
    return comment_core.delete_user_comment(db=db, user=panel_user, comment_id=comment_id)
