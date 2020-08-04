import pytest
import tempfile
import os
import datetime
from backend import app as backend
from backend.schema import schema
from backend.models import Salary
from graphene.test import Client


def generate_data():
    backend.app.secret_key = "sekrit!"
    backend.db.drop_all()
    backend.db.create_all()
    s1 = Salary(
        case_number="1",
        case_status="test",
        visa_class="test",
        job_title="engineer",
        full_time_position="y",
        employment_start_date=datetime.datetime(2020, 8, 1),
        employer_name="google",
        prevailing_wage=100000.0,
        employer_city="sf",
        employer_state="ca",
    )
    s2 = Salary(
        case_number="2",
        case_status="test",
        visa_class="test",
        job_title="engineer",
        full_time_position="y",
        employment_start_date=datetime.datetime(2020, 8, 1),
        employer_name="apple",
        prevailing_wage=200000.0,
        employer_city="sf",
        employer_state="ca",
    )
    backend.db.session.add_all([s1, s2])
    backend.db.session.commit()


def set_session(client, employer="", title="", city="", state="", year=""):
    with client.session_transaction() as sess:
        sess["employer"] = employer
        sess["title"] = title
        sess["city"] = city
        sess["state"] = state
        sess["year"] = year


@pytest.fixture
def graphql_client():
    db_fd, backend.app.config["DATABASE"] = tempfile.mkstemp()
    backend.app.config["TESTING"] = True
    with backend.app.app_context():
        generate_data()
    yield Client(schema)
    os.close(db_fd)
    os.unlink(backend.app.config["DATABASE"])


@pytest.fixture
def client():
    db_fd, backend.app.config["DATABASE"] = tempfile.mkstemp()
    backend.app.config["TESTING"] = True
    with backend.app.test_client() as client:
        with backend.app.app_context():
            generate_data()
        yield client
    os.close(db_fd)
    os.unlink(backend.app.config["DATABASE"])
