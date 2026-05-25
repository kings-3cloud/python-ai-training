from typing import Annotated

from fastapi import Depends
from sqlmodel import create_engine, SQLModel, Session


sqlite_full_name = "database.db"
connectionString = f"sqlite:///{sqlite_full_name}"

connection_args = { "check_same_thread": False }
engine = create_engine(connectionString, connect_args=connection_args)

def create_db_and_table():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
