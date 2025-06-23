from sqlmodel import SQLModel, create_engine, Session

# SQLite file-based DB
sqlite_url = "sqlite:///./products.db"
engine = create_engine(sqlite_url, echo=True)

def create_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
