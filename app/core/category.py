from fastapi import HTTPException, status
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.enums import Status
from app.helpers.error_helper import Error
from app.models import Category
from app.schemas.admin.category import CategoryIn


class CategoryCore:
    def __init__(self):
        pass

    def get_category_by_id(self, db: Session, category_id: int, only_active=True):
        filter_array = [Category.id == category_id, Category.status != Status.deleted]
        if only_active:
            filter_array.append(Category.status == Status.active)
        category = db.query(Category).filter(*filter_array).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=Error.record_not_found)
        return category

    def get_all_categories(self, db: Session):
        # sadece active ve passive kategoriler
        return db.query(Category).filter(and_(Category.status != Status.deleted)).all()

    def create_category(self, db: Session, data: CategoryIn):
        # Aynı isimde kategori varsa hata döndür
        existing = db.query(Category).filter(Category.name == data.name, Category.status != Status.deleted).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Category with this name already exists."
            )

        category = Category(
            name=data.name,
            status=data.status or Status.passive,
        )
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    def update_category(self, db: Session, category_id: int, data: CategoryIn):
        category = self.get_category_by_id(db=db, category_id=category_id, only_active=False)

        # İsim değiştirilecekse, aynı isim başka kategori var mı kontrol et
        if data.name != category.name:
            existing = (
                db.query(Category)
                .filter(Category.name == data.name, Category.id != category_id, Category.status != Status.deleted)
                .first()
            )
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Category with this name already exists."
                )

        category.name = data.name
        category.status = data.status or category.status

        db.commit()
        db.refresh(category)
        return category

    def delete_category(self, db: Session, category_id: int):
        category = self.get_category_by_id(db=db, category_id=category_id, only_active=False)
        category.status = Status.deleted  # Soft delete
        db.commit()
        return {"message": "Category deleted successfully."}


category_core = CategoryCore()
