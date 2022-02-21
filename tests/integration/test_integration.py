import pytest
import server
from server import app
from flask import template_rendered
from contextlib import contextmanager


@contextmanager
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))
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
            rv = app.test_client().post('/showSummary', data=data)
            assert rv.status_code == 200
            assert len(templates) == 1
            template, context = templates[0]
            assert template.name == 'welcome.html'

            # book places
            initial_club_points = int(club['points'])
            places = 0
            if int(club['points']) < int(competition['numberOfPlaces']):
                places = int(club['points'])
            else:
                places = int(competition['numberOfPlaces'])
            data = {'places': places, 'club': club['name'],
                    'competition': competition['name']}
            rv = app.test_client().post('/purchasePlaces', data=data)
            # assert new cub nb of points
            assert rv.status_code == 200
            assert len(templates) == 2
            template, context = templates[1]
            assert template.name == 'welcome.html'
            assert int(club['points']) == initial_club_points - places

    def test_login_book_past_competition_should_return_error_message(self, client, clubs_fixture, past_competitions_fixture, mocker):
        mocker.patch.object(server, 'clubs', clubs_fixture['clubs'])
        mocker.patch.object(server, 'competitions',
                            past_competitions_fixture['competitions'])
        club = clubs_fixture['clubs'][0]
        competition = past_competitions_fixture['competitions'][0]

        with captured_templates(app) as templates:
            # login
            data = {'email': club['email']}
            rv = app.test_client().post('/showSummary', data=data)
            assert rv.status_code == 200
            assert len(templates) == 1
            template, context = templates[0]
            assert template.name == 'welcome.html'
            # book past competition
            data = {'competition': competition['name']}
            url = f"/book/{competition['name'].replace(' ', '%20')}/{club['name'].replace(' ', '%20')}"
            rv = app.test_client().post(url, data=data)
            assert rv.status_code == 200
            assert len(templates) == 2
            template, context = templates[1]
            assert template.name == 'welcome.html'
            assert b'sorry, this competition allready took place' in rv.data

    def test_login_book_more_than_12_places_should_return_error_message(self, client, clubs_fixture, competitions_fixture, mocker):
        mocker.patch.object(server, 'clubs', clubs_fixture['clubs'])
        mocker.patch.object(server, 'competitions',
                            competitions_fixture['competitions'])
        club = clubs_fixture['clubs'][0]
        competition = competitions_fixture['competitions'][0]

        with captured_templates(app) as templates:
            # login
            data = {'email': club['email']}
            rv = app.test_client().post('/showSummary', data=data)
            assert rv.status_code == 200
            assert len(templates) == 1
            template, context = templates[0]
            assert template.name == 'welcome.html'

            # book places
            data = {'places': 13, 'club': club['name'],
                    'competition': competition['name']}
            rv = app.test_client().post('/purchasePlaces', data=data)
            assert rv.status_code == 200
            assert len(templates) == 2
            template, context = templates[1]
            assert template.name == 'welcome.html'
            assert b'sorry, you cannot purchase more than 12 places' in rv.data

    def test_login_points_board_should_return_200(self, client, clubs_fixture, mocker):
        mocker.patch.object(server, 'clubs', clubs_fixture['clubs'])
        club = clubs_fixture['clubs'][0]

        with captured_templates(app) as templates:
            # login
            data = {'email': club['email']}
            rv = app.test_client().post('/showSummary', data=data)
            assert rv.status_code == 200
            assert len(templates) == 1
            template, context = templates[0]
            assert template.name == 'welcome.html'

            # Board display
            rv = app.test_client().get('/board')
            assert rv.status_code == 200
            assert len(templates) == 2
            template, context = templates[1]
            assert template.name == 'board.html'
