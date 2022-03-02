import pytest
import server


@pytest.fixture
def client():
    '''this is the fixture that sets a client for the tests'''
    with server.app.test_client() as client:
        yield client


@pytest.fixture
def clubs_fixture():
    '''this is the fixture that sets a fake list of clubs for the tests'''
    clubs = {
        "clubs": [
            {"name": "club_A", "email": "club_a@club_a.com", "points": 10},
            {"name": "club_B", "email": "club_b@club_b.com", "points": 12},
            {"name": "club_C", "email": "club_c@club_c.com", "points": 7},
        ]
    }
    return clubs


@pytest.fixture
def competitions_fixture():
    '''this is the fixture that sets a fake list of competitions for the tests'''
    competitions = {
        "competitions": [
            {
                "name": "Test compet A",
                "date": "2020-03-27 10:00:00",
                "numberOfPlaces": "25",
            },
            {
                "name": "Test compet B",
                "date": "2020-10-22 13:30:00",
                "numberOfPlaces": "13",
            },
        ]
    }
    return competitions


@pytest.fixture
def past_competitions_fixture():
    '''this is the fixture that sets a fake list of future and past competitions for the tests'''
    competitions = {
        "competitions": [
            {
                "name": "Test past compet",
                "date": "2020-10-22 13:30:00",
                "numberOfPlaces": "13",
            },
            {
                "name": "Test future compet",
                "date": "2024-10-22 13:30:00",
                "numberOfPlaces": "13",
            },
        ]
    }
    return competitions


@pytest.fixture
def no_competitions_fixture():
    '''this is the fixture that sets an empty list of competitions for the tests'''
    competitions = {"competitions": []}
    return competitions


@pytest.fixture
def no_clubs_fixture():
    '''this is the fixture that sets an empty list of clubs for the tests'''
    clubs = {"clubs": []}
    return clubs
