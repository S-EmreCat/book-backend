from fastapi import HTTPException, status
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
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=Error.category_not_found)
        return category

    # status parametresi ile aktif/pasif tüm kategoriler veya sadece aktif kategoriler getirilebilir
    def get_all_categories(self, db: Session, status: Status = None):
        query = db.query(Category).filter(Category.status != Status.deleted)
        if status is not None:
            query = query.filter(Category.status == status)
        # sadece active ve passive kategoriler
        return query

    def create_category(self, db: Session, data: CategoryIn):
        # Aynı isimde kategori varsa hata döndür
        existing = db.query(Category).filter(Category.name == data.name, Category.status != Status.deleted).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=Error.category_name_exists,
            )

        category = Category(
            name=data.name,
            status=data.status,
        )
        db.add(category)
        db.commit()
        return category

    def update_category(self, db: Session, category_id: int, data: CategoryIn):
        category = self.get_category_by_id(db=db, category_id=category_id, only_active=False)

        # İsim değiştirilecekse, aynı isim başka kategori var mı kontrol et
        if data.name != category.name:
            existing = (
                db.query(Category)
                .filter(
                    Category.name == data.name,
                    Category.id != category_id,
                    Category.status != Status.deleted,
                )
                .first()
            )
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=Error.category_name_exists,
                )

        category.name = data.name
        category.status = data.status
        db.commit()
        return category

    def delete_category(self, db: Session, category_id: int):
        category = self.get_category_by_id(db=db, category_id=category_id, only_active=False)
        category.status = Status.deleted  # Soft delete
        db.commit()
        return {"message": "Category deleted successfully."}


category_core = CategoryCore()
