import pytest
import flask
from client import client, set_session


def test_table_returns_data(client):
    set_session(client)
    resp = client.get("/table?limit=10&offset=0", follow_redirects=True)
    assert resp.json == {
        "rows": [
            {
                "case_number": "1",
                "case_status": "test",
                "employer_city": "sf",
                "employer_name": "google",
                "employer_state": "ca",
                "employment_start_date": "Sat, 01 Aug 2020 00:00:00 GMT",
                "full_time_position": "y",
                "job_title": "engineer",
                "prevailing_wage": 100000.0,
                "visa_class": "test",
            },
            {
                "case_number": "2",
                "case_status": "test",
                "employer_city": "sf",
                "employer_name": "apple",
                "employer_state": "ca",
                "employment_start_date": "Sat, 01 Aug 2020 00:00:00 GMT",
                "full_time_position": "y",
                "job_title": "engineer",
                "prevailing_wage": 200000.0,
                "visa_class": "test",
            },
        ],
        "total": 2,
    }
