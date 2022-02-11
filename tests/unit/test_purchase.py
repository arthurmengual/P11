import pytest
import server
from datetime import datetime


class Testpurchase:
    def test_book_past_competition_should_return_error_message(self, client, clubs_fixture, competitions_fixture, mocker):
        mocker.patch.object(server, 'competitions',
                            competitions_fixture)
        mocker.patch.object(server, 'clubs',
                            clubs_fixture)
        competition = [comp for comp in competitions_fixture['competitions']
                       if comp['name'] == 'Test past compet'][0]
        club = clubs_fixture['clubs'][0]
        data = {'club': club, 'competitions': competition}
        response = client.post(
            f"/book/{competition['name']}/{club['name']}", data=data)

        assert b'sorry, this competition allready took place' in response.data

    def test_book_future_competition_should_return_error_message(self, client, clubs_fixture, competitions_fixture, mocker):
        mocker.patch.object(server, 'competitions',
                            competitions_fixture)
        mocker.patch.object(server, 'clubs',
                            clubs_fixture)
        competition = [comp for comp in competitions_fixture['competitions']
                       if comp['name'] == 'Test future compet'][0]
        club = clubs_fixture['clubs'][0]
        data = {'club': club['name'], 'competitions': competition['name']}
        response = client.post(
            f"/book/{competition['name']}/{club['name']}", data=data)

        assert response.status_code == 200
        assert b'sorry, this competition allready took place' not in response.data
