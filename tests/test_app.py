from client import client, set_session


def test_table_endpoint_returns_data(client):
    set_session(client)
    resp = client.get("/table?limit=10&offset=0")
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


def test_table_endpoint_returns_queried_data(client):
    set_session(client, employer="google", title="engineer")
    resp = client.get("/table?limit=10&offset=0")
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
            }
        ],
        "total": 1,
    }


def test_data_endpoint_returns_queried_data(client):
    resp = client.get("/data?field1=job_title&value1=engineer")
    assert resp.json == {
        "results": [
            {
                "case_number": "1",
                "case_status": "test",
                "employer_city": "sf",
                "employer_name": "google",
                "employer_state": "ca",
                "employment_start_date": "2020-08-01",
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
                "employment_start_date": "2020-08-01",
                "full_time_position": "y",
                "job_title": "engineer",
                "prevailing_wage": 200000.0,
                "visa_class": "test",
            },
        ],
    }
