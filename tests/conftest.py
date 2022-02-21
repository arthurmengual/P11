import pytest
import server


@pytest.fixture
def client():
    with server.app.test_client() as client:
        yield client


@pytest.fixture
def clubs_fixture():
    clubs = {'clubs': [{'name': 'club_A', 'email': 'club_a@club_a.com', 'points': 5},
                       {'name': 'club_B', 'email': 'club_b@club_b.com', 'points': 12},
                       {'name': 'club_C', 'email': 'club_c@club_c.com', 'points': 7}
                       ]
             }
    return clubs


@pytest.fixture
def competitions_fixture():
    competitions = {'competitions': [
        {
            "name": "Test compet A",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Test compet B",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        },
    ]}
    return competitions


@pytest.fixture
def past_competitions_fixture():
    competitions = {'competitions': [
        {
            "name": "Test past compet",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        },
        {
            "name": "Test future compet",
            "date": "2024-10-22 13:30:00",
            "numberOfPlaces": "13"
        }
    ]}
    return competitions


@pytest.fixture
def no_competitions_fixture():
    competitions = {'competitions': [
    ]}
    return competitions


@pytest.fixture
def no_clubs_fixture():
    clubs = {'clubs': [
    ]}
    return clubs
