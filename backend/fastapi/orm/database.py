from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def db_init():
    Base.metadata.create_all(bind=engine)

def db_test():
    try:
        with engine.connect() as connection:
            print("Successfully connected to the database!")
    except Exception as e:
        print(f"An error occurred: {e}")
    db_init()
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    if 'users' in tables:
        print("The 'users' table exists.")
    else:
        print("The 'users' table does not exist.")
    