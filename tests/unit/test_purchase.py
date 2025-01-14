import server
from server import app
from flask import template_rendered
from contextlib import contextmanager
import math


@contextmanager
def captured_templates(app):
    '''This function captures the templates to further verify which one was rendered'''
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


class TestPurchase:
    def test_more_than_12_points_should_return_error_message(
        self, client, clubs_fixture, competitions_fixture, mocker
    ):
        '''This test creates a client, trie to book more than the authorized amount
        of points to a competition and verifies the status_code, template rendered and error message'''
        mocker.patch.object(server, "clubs", clubs_fixture["clubs"])
        mocker.patch.object(
            server, "competitions", competitions_fixture["competitions"]
        )
        club = clubs_fixture["clubs"][0]
        competition = competitions_fixture["competitions"][0]
        data = {"places": 13, "club": club["name"], "competition": competition["name"]}

        with captured_templates(app) as templates:
            response = client.post("/purchasePlaces", data=data)
            assert response.status_code == 200
            assert b"sorry, you cannot purchase more than 12 places" in response.data
            assert len(templates) == 1
            template = templates[0]
            assert template.name == "welcome.html"

    def test_12_points_should_return_200(
        self, client, clubs_fixture, competitions_fixture, mocker
    ):
        '''This test creates a client, trie to book the authorized amount
        of points to a competition and verifies the status_code, template rendered'''
        mocker.patch.object(server, "clubs", clubs_fixture["clubs"])
        mocker.patch.object(
            server, "competitions", competitions_fixture["competitions"]
        )
        club = clubs_fixture["clubs"][0]
        competition = competitions_fixture["competitions"][0]
        data = {"places": 12, "club": club["name"], "competition": competition["name"]}

        with captured_templates(app) as templates:
            response = client.post("/purchasePlaces", data=data)
            assert response.status_code == 200
            assert (
                b"sorry, you cannot purchase more than 12 places" not in response.data
            )

            assert len(templates) == 1
            template = templates[0]
            assert template.name == "welcome.html"

    def test_less_than_12_points_should_return_200(
        self, client, clubs_fixture, competitions_fixture, mocker
    ):
        '''This test creates a client, trie to book less than the authorized amount
        of points to a competition and verifies the status_code, template rendered'''
        mocker.patch.object(server, "clubs", clubs_fixture["clubs"])
        mocker.patch.object(
            server, "competitions", competitions_fixture["competitions"]
        )
        club = clubs_fixture["clubs"][0]
        competition = competitions_fixture["competitions"][0]
        data = {"places": 11, "club": club["name"], "competition": competition["name"]}

        with captured_templates(app) as templates:
            response = client.post("/purchasePlaces", data=data)
            assert response.status_code == 200
            assert (
                b"sorry, you cannot purchase more than 12 places" not in response.data
            )
            assert len(templates) == 1
            template = templates[0]
            assert template.name == "welcome.html"

    def test_more_than_club_points_should_return_error_message(
        self, client, clubs_fixture, competitions_fixture, mocker
    ):
        '''This test creates a client, trie to book more than the club amount
        of points to a competition and verifies the status_code, template rendered and error message'''
        mocker.patch.object(server, "clubs", clubs_fixture["clubs"])
        mocker.patch.object(
            server, "competitions", competitions_fixture["competitions"]
        )
        club = clubs_fixture["clubs"][0]
        competition = competitions_fixture["competitions"][0]
        data = {
            "places": int(club["points"] + 1),
            "club": club["name"],
            "competition": competition["name"],
        }

        with captured_templates(app) as templates:
            response = client.post("/purchasePlaces", data=data)
            assert response.status_code == 200
            assert b"sorry, you do not have enough points" in response.data
            assert len(templates) == 1
            template = templates[0]
            assert template.name == "welcome.html"

    def test_less_club_points_should_return_error_message(
        self, client, clubs_fixture, competitions_fixture, mocker
    ):
        '''This test creates a client, trie to book less than the club amount
        of points to a competition and verifies the status_code, template rendered and error message'''
        mocker.patch.object(server, "clubs", clubs_fixture["clubs"])
        mocker.patch.object(
            server, "competitions", competitions_fixture["competitions"]
        )
        club = clubs_fixture["clubs"][0]
        competition = competitions_fixture["competitions"][0]
        places = math.floor(int(club["points"]) / 3) - 1
        data = {
            "places": places,
            "club": club["name"],
            "competition": competition["name"],
        }

        with captured_templates(app) as templates:
            response = client.post("/purchasePlaces", data=data)
            assert response.status_code == 200
            assert b"sorry, you do not have enough points" not in response.data
            assert len(templates) == 1
            template = templates[0]
            assert template.name == "welcome.html"

    def test_equal_club_points_should_return_error_message(
        self, client, clubs_fixture, competitions_fixture, mocker
    ):
        '''This test creates a client, trie to book the club amount
        of points to a competition and verifies the status_code, template rendered and error message'''
        mocker.patch.object(server, "clubs", clubs_fixture["clubs"])
        mocker.patch.object(
            server, "competitions", competitions_fixture["competitions"]
        )
        club = clubs_fixture["clubs"][0]
        competition = competitions_fixture["competitions"][0]
        places = math.floor(int(club["points"]) / 3)
        data = {
            "places": places,
            "club": club["name"],
            "competition": competition["name"],
        }

        with captured_templates(app) as templates:
            response = client.post("/purchasePlaces", data=data)
            assert response.status_code == 200
            assert b"sorry, you do not have enough points" not in response.data
            assert len(templates) == 1
            template = templates[0]
            assert template.name == "welcome.html"

    def test_points_should_be_updated(
        self, client, clubs_fixture, competitions_fixture, mocker
    ):
        '''This test creates a client, book places to a competition and verifies the status_code,
        template rendered and the new amount of club's points'''
        mocker.patch.object(server, "clubs", clubs_fixture["clubs"])
        mocker.patch.object(
            server, "competitions", competitions_fixture["competitions"]
        )
        club = clubs_fixture["clubs"][0]
        initial_points = club["points"]
        competition = competitions_fixture["competitions"][0]
        nb_of_places = 2
        data = {
            "club": club["name"],
            "competition": competition["name"],
            "places": nb_of_places,
        }

        with captured_templates(app) as templates:
            response = client.post("/purchasePlaces", data=data)
            updated_points = club["points"]
            expected_points = int(initial_points) - nb_of_places * 3
            assert response.status_code == 200
            assert updated_points == expected_points
            assert len(templates) == 1
            template = templates[0]
            assert template.name == "welcome.html"

    def test_book_past_competition_should_return_error_message(
        self, client, clubs_fixture, past_competitions_fixture, mocker
    ):
        '''This test creates a client, trie to book places to a past competition
        and verifies the status_code, template rendered and error message'''
        mocker.patch.object(
            server, "competitions", past_competitions_fixture["competitions"]
        )
        mocker.patch.object(server, "clubs", clubs_fixture["clubs"])
        competition = [
            comp
            for comp in past_competitions_fixture["competitions"]
            if comp["name"] == "Test past compet"
        ][0]
        club = clubs_fixture["clubs"][0]
        data = {"club": club["name"], "competitions": competition["name"]}
        url = f"/book/{competition['name'].replace(' ', '%20')}/{club['name'].replace(' ', '%20')}"

        with captured_templates(app) as templates:
            response = client.post(url, data=data)
            assert response.status_code == 200
            assert b"sorry, this competition allready took place" in response.data
            assert len(templates) == 1
            template = templates[0]
            assert template.name == "welcome.html"

    def test_book_future_competition_should_return_error_message(
        self, client, clubs_fixture, past_competitions_fixture, mocker
    ):
        '''This test creates a client, trie to book places to a future competition
        and verifies the status_code, template rendered'''
        mocker.patch.object(
            server, "competitions", past_competitions_fixture["competitions"]
        )
        mocker.patch.object(server, "clubs", clubs_fixture["clubs"])
        competition = [
            comp
            for comp in past_competitions_fixture["competitions"]
            if comp["name"] == "Test future compet"
        ][0]
        club = clubs_fixture["clubs"][0]
        data = {"club": club["name"], "competitions": competition["name"]}
        url = f"/book/{competition['name'].replace(' ', '%20')}/{club['name'].replace(' ', '%20')}"

        with captured_templates(app) as templates:
            response = client.post(url, data=data)
            assert response.status_code == 200
            assert b"sorry, this competition allready took place" not in response.data
            assert len(templates) == 1
            template = templates[0]
            assert template.name == "booking.html"

    def test_no_competition_to_book(
        self,
        client,
        clubs_fixture,
        competitions_fixture,
        no_competitions_fixture,
        mocker,
    ):
        '''This test creates a client, trie to book places when there are no competition available
        and verifies the status_code, template rendered and error message'''
        mocker.patch.object(
            server, "competitions", no_competitions_fixture["competitions"]
        )
        mocker.patch.object(server, "clubs", clubs_fixture["clubs"])
        competition = competitions_fixture["competitions"][0]
        club = clubs_fixture["clubs"][0]
        data = {"club": club["name"], "competitions": competition["name"]}
        url = f"/book/{competition['name'].replace(' ', '%20')}/{club['name'].replace(' ', '%20')}"

        with captured_templates(app) as templates:
            response = client.post(url, data=data)
            assert response.status_code == 200
            assert b"Something went wrong-please try again" in response.data
            assert len(templates) == 1
            template = templates[0]
            assert template.name == "welcome.html"

    def test_no_club_to_book(
        self, client, clubs_fixture, competitions_fixture, no_clubs_fixture, mocker
    ):
        '''This test creates a client, trie to book places when there are no club available
        and verifies the status_code, template rendered and error message'''
        mocker.patch.object(
            server, "competitions", competitions_fixture["competitions"]
        )
        mocker.patch.object(server, "clubs", no_clubs_fixture["clubs"])
        competition = competitions_fixture["competitions"][0]
        club = clubs_fixture["clubs"][0]
        data = {"club": club["name"], "competitions": competition["name"]}
        url = f"/book/{competition['name'].replace(' ', '%20')}/{club['name'].replace(' ', '%20')}"

        with captured_templates(app) as templates:
            response = client.post(url, data=data)
            print('yoyo', response.data)
            assert response.status_code == 200
            assert b"Something went wrong-please try again" in response.data
            assert len(templates) == 1
            template = templates[0]
            assert template.name == "welcome.html"

    def test_no_club_no_competition_to_book(
        self,
        client,
        clubs_fixture,
        competitions_fixture,
        no_clubs_fixture,
        no_competitions_fixture,
        mocker,
    ):
        '''This test creates a client, trie to book places when there are no competition and no club
        available and verifies the status_code, template rendered and error message'''
        mocker.patch.object(
            server, "competitions", no_competitions_fixture["competitions"]
        )
        mocker.patch.object(server, "clubs", no_clubs_fixture["clubs"])
        competition = competitions_fixture["competitions"][0]
        club = clubs_fixture["clubs"][0]
        data = {"club": club["name"], "competitions": competition["name"]}
        url = f"/book/{competition['name'].replace(' ', '%20')}/{club['name'].replace(' ', '%20')}"

        with captured_templates(app) as templates:
            response = client.post(url, data=data)
            assert b"Something went wrong-please try again" in response.data
            assert response.status_code == 200
            assert len(templates) == 1
            template = templates[0]
            assert template.name == "welcome.html"
