import pytest
import server


@pytest.fixture
def client():
    with server.app.test_client() as client:
        yield client


@pytest.fixture
def clubs_fixture():
    clubs = {'clubs': [{'name': 'club_A', 'email': 'club_a@club_a.com', 'points': 20},
                       {'name': 'club_B', 'email': 'club_b@club_b.com', 'points': 20},
                       {'name': 'club_C', 'email': 'club_c@club_c.com', 'points': 20}
                       ]
             }
    return clubs
