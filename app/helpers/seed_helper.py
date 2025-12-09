from sqlalchemy.orm.session import Session

from app import models
from app.database import seed_data


def initial_seed(db: Session):
    db.bulk_save_objects([models.AdminUser(**c) for c in seed_data.admin_user])
    db.flush()

    db.bulk_save_objects([models.Category(**c) for c in seed_data.categories])
    db.flush()

    db.bulk_save_objects([models.Author(**c) for c in seed_data.authors])
    db.flush()

    db.bulk_save_objects([models.Publisher(**c) for c in seed_data.publishers])
    db.flush()

    db.bulk_save_objects([models.Book(**c) for c in seed_data.books])
    db.flush()

    db.commit()
    return "DONE"
