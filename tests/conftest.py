import sys
import os

# Add src folder to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import pytest
from app import create_app
from extensions import db


@pytest.fixture
def app():

    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "MONGO_URI": "mongodb://localhost:27017/test_db"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()