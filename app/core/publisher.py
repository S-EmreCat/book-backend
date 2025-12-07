from fastapi import HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from app.enums import Status
from app.helpers.error_helper import Error
from app.models.publisher import Publisher
from app.schemas.admin.publisher import PublisherIn


class PublisherCore:
    def __init__(self):
        pass

    def get_publisher_by_id(self, db: Session, publisher_id: int, only_active=True):
        filter_array = [Publisher.id == publisher_id, Publisher.status != Status.deleted]
        if only_active:
            filter_array.append(Publisher.status == Status.active)
        publisher = db.query(Publisher).filter(*filter_array).first()
        if not publisher:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=Error.publisher_not_found)
        return publisher

    def get_all_publishers(self, db: Session, only_active=True):
        query = db.query(Publisher).filter(Publisher.status != Status.deleted)
        if only_active:
            query = query.filter(Publisher.status == Status.active)
        return paginate(query)

    def create_publisher(self, db: Session, data: PublisherIn):
        existing = db.query(Publisher).filter(Publisher.name == data.name, Publisher.status != Status.deleted).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=Error.publisher_already_exists,
            )

        publisher = Publisher(name=data.name, status=data.status or Status.passive)
        db.add(publisher)
        db.commit()
        return publisher

    def update_publisher(self, db: Session, publisher_id: int, data: PublisherIn):
        publisher = self.get_publisher_by_id(db=db, publisher_id=publisher_id, only_active=False)

        if data.name != publisher.name:
            existing = (
                db.query(Publisher)
                .filter(
                    Publisher.name == data.name,
                    Publisher.id != publisher_id,
                    Publisher.status != Status.deleted,
                )
                .first()
            )
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=Error.publisher_already_exists,
                )

        publisher.name = data.name
        publisher.status = data.status
        db.commit()
        return publisher

    def delete_publisher(self, db: Session, publisher_id: int):
        publisher = self.get_publisher_by_id(db=db, publisher_id=publisher_id, only_active=False)
        publisher.status = Status.deleted
        db.commit()
        return {"message": "Publisher deleted successfully."}


publisher_core = PublisherCore()
