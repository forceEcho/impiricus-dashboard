from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, delete

from app.core.db import engine, init_db
from app.main import app
from app.models import Physician, Message, ClassificationRule, RuleKeyword


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        init_db()
        yield session

        # Teardown: remove test data
        statement=delete(Message)  
        session.execute(statement)
        statement=delete(Physician)  
        session.execute(statement)
        statement=delete(RuleKeyword)  
        session.execute(statement)
        statement=delete(ClassificationRule)  
        session.execute(statement) 
        session.commit()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c
