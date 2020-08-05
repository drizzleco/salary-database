from client import graphql_client


def test_resolve_salaries(graphql_client):
    executed = graphql_client.execute(
        """
        {
        salaries(employer: "google", title: "engineer") {
            caseNumber
            employerName
            jobTitle
            prevailingWage
            employerCity
            employerState
        }
        }
        """
    )
    assert executed == {
        "data": {
            "salaries": [
                {
                    "caseNumber": "1",
                    "employerName": "google",
                    "jobTitle": "engineer",
                    "prevailingWage": 100000.0,
                    "employerCity": "sf",
                    "employerState": "ca",
                }
            ]
        }
    }
