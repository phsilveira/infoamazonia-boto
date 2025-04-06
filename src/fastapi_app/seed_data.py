from sqlmodel import SQLModel

try:
    from fastapi_app.models import Restaurant, Review, create_db_and_tables, engine
except ImportError:
    # For when running directly from this directory
    from .models import Restaurant, Review, create_db_and_tables, engine


def drop_all():
    # Explicitly remove these tables first to avoid cascade errors
    SQLModel.metadata.remove(Restaurant.__table__)
    SQLModel.metadata.remove(Review.__table__)
    SQLModel.metadata.drop_all(engine)


if __name__ == "__main__":
    print("Creating database and tables...")
    create_db_and_tables()
    print("Database and tables created successfully!")
