import pytest
import server
from server import app
from flask import template_rendered
from contextlib import contextmanager


@contextmanager
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


class Test_integration:
    def test_login_book_places_should_return_200(self, client, clubs_fixture, competitions_fixture, mocker):
        mocker.patch.object(server, 'clubs', clubs_fixture['clubs'])
        mocker.patch.object(server, 'competitions',
                            competitions_fixture['competitions'])
        club = clubs_fixture['clubs'][0]
        competition = competitions_fixture['competitions'][0]

        with captured_templates(app) as templates:
            # login
            data = {'email': club['email']}
            response = client.post('/showSummary', data=data)
            assert response.status_code == 200
            assert len(templates) == 1
            template = templates[0]
            assert template.name == 'welcome.html'

            # book places
            initial_club_points = int(club['points'])
            places = 1
            data = {'places': places, 'club': club['name'],
                    'competition': competition['name']}
            response = client.post('/purchasePlaces', data=data)
            # assert new cub nb of points
            assert response.status_code == 200
            assert len(templates) == 2
            template = templates[1]
            assert template.name == 'welcome.html'
            assert int(club['points']) == initial_club_points - places*3

    def test_login_book_past_competition_should_return_error_message(self, client, clubs_fixture, past_competitions_fixture, mocker):
        mocker.patch.object(server, 'clubs', clubs_fixture['clubs'])
        mocker.patch.object(server, 'competitions',
                            past_competitions_fixture['competitions'])
        club = clubs_fixture['clubs'][0]
        competition = past_competitions_fixture['competitions'][0]

        with captured_templates(app) as templates:
            # login
            data = {'email': club['email']}
            response = client.post('/showSummary', data=data)
            assert response.status_code == 200
            assert len(templates) == 1
            template = templates[0]
            assert template.name == 'welcome.html'
            # book past competition
            data = {'competition': competition['name']}
            url = f"/book/{competition['name'].replace(' ', '%20')}/{club['name'].replace(' ', '%20')}"
            response = app.test_client().post(url, data=data)
            assert response.status_code == 200
            assert len(templates) == 2
            template = templates[1]
            assert template.name == 'welcome.html'
            assert b'sorry, this competition allready took place' in response.data

    def test_login_book_more_than_12_places_should_return_error_message(self, client, clubs_fixture, competitions_fixture, mocker):
        mocker.patch.object(server, 'clubs', clubs_fixture['clubs'])
        mocker.patch.object(server, 'competitions',
                            competitions_fixture['competitions'])
        club = clubs_fixture['clubs'][0]
        competition = competitions_fixture['competitions'][0]

        with captured_templates(app) as templates:
            # login
            data = {'email': club['email']}
            response = client.post('/showSummary', data=data)
            assert response.status_code == 200
            assert len(templates) == 1
            template = templates[0]
            assert template.name == 'welcome.html'

            # book places
            data = {'places': 13, 'club': club['name'],
                    'competition': competition['name']}
            response = client.post('/purchasePlaces', data=data)
            assert response.status_code == 200
            assert len(templates) == 2
            template = templates[1]
            assert template.name == 'welcome.html'
            assert b'sorry, you cannot purchase more than 12 places' in response.data

    def test_login_points_board_should_return_200(self, client, clubs_fixture, mocker):
        mocker.patch.object(server, 'clubs', clubs_fixture['clubs'])
        club = clubs_fixture['clubs'][0]

        with captured_templates(app) as templates:
            # login
            data = {'email': club['email']}
            response = client.post('/showSummary', data=data)
            assert response.status_code == 200
            assert len(templates) == 1
            template = templates[0]
            assert template.name == 'welcome.html'

            # Board display
            response = client.get('/board')
            assert response.status_code == 200
            assert len(templates) == 2
            template = templates[1]
            assert template.name == 'board.html'
