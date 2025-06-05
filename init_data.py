from app.database.database import SessionLocal
from app.helpers import seed_helper


def upgrade():
    print("Started: init_data")  # noqa: T201
    session = SessionLocal()
    seed_helper.initial_seed(db=session)
    print("Finished: init_data")  # noqa: T201


upgrade()
