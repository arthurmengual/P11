import pytest
import server
<< << << < HEAD


class Testpurchase:
    def test_more_than_12_points_should_return_error_message(self, client, clubs_fixture, competitions_fixture, mocker):
        mocker.patch.object(server, 'clubs', clubs_fixture['clubs'])
        mocker.patch.object(server, 'competitions',
                            competitions_fixture['competitions'])
        club = clubs_fixture['clubs'][0]
        initial_points = club['points']
        competition = competitions_fixture['competitions'][0]
        data = {'places': 13, 'club': club['name'],
                'competition': competition['name']}
        response = client.post('/purchasePlaces', data=data)

        assert b'sorry, you cannot purchase more than 12 places' in response.data

    def test_12_points_should_return_200(self, client, clubs_fixture, competitions_fixture, mocker):
        mocker.patch.object(server, 'clubs', clubs_fixture['clubs'])
        mocker.patch.object(server, 'competitions',
                            competitions_fixture['competitions'])
        club = clubs_fixture['clubs'][0]
        competition = competitions_fixture['competitions'][0]
        data = {'places': 12, 'club': club['name'],
                'competition': competition['name']}
        response = client.post('/purchasePlaces', data=data)

        assert b'sorry, you cannot purchase more than 12 places' not in response.data
        assert response.status_code == 200

    def test_less_than_12_points_should_return_200(self, client, clubs_fixture, competitions_fixture, mocker):
        mocker.patch.object(server, 'clubs', clubs_fixture['clubs'])
        mocker.patch.object(server, 'competitions',
                            competitions_fixture['competitions'])
        club = clubs_fixture['clubs'][0]
        competition = competitions_fixture['competitions'][0]
        data = {'places': 11, 'club': club['name'],
                'competition': competition['name']}
        response = client.post('/purchasePlaces', data=data)

        assert b'sorry, you cannot purchase more than 12 places' not in response.data
        assert response.status_code == 200

    def test_more_than_club_points_should_return_error_message(self, client, clubs_fixture, competitions_fixture, mocker):
        mocker.patch.object(server, 'clubs', clubs_fixture['clubs'])
        mocker.patch.object(server, 'competitions',
                            competitions_fixture['competitions'])
        club = clubs_fixture['clubs'][0]
        competition = competitions_fixture['competitions'][0]
        data = {'places': int(
            club['points']+1), 'club': club['name'], 'competition': competition['name']}
        response = client.post('/purchasePlaces', data=data)
        print(response.data)

        assert b'sorry, you do not have enough points' in response.data

    def test_less_club_points_should_return_error_message(self, client, clubs_fixture, competitions_fixture, mocker):
        mocker.patch.object(server, 'clubs', clubs_fixture['clubs'])
        mocker.patch.object(server, 'competitions',
                            competitions_fixture['competitions'])
        club = clubs_fixture['clubs'][0]
        competition = competitions_fixture['competitions'][0]
        data = {'places': int(
            club['points']), 'club': club['name'], 'competition': competition['name']}
        response = client.post('/purchasePlaces', data=data)

        assert b'sorry, you do not have enough points' not in response.data
        assert response.status_code == 200

    def test_equal_club_points_should_return_error_message(self, client, clubs_fixture, competitions_fixture, mocker):
        mocker.patch.object(server, 'clubs', clubs_fixture['clubs'])
        mocker.patch.object(server, 'competitions',
                            competitions_fixture['competitions'])
        club = clubs_fixture['clubs'][0]
        competition = competitions_fixture['competitions'][0]
        data = {'places': int(
            club['points']-1), 'club': club['name'], 'competition': competition['name']}
        response = client.post('/purchasePlaces', data=data)

        assert b'sorry, you do not have enough points' not in response.data
        assert response.status_code == 200

    def test_points_should_be_updated(self, client, clubs_fixture, competitions_fixture, mocker):
        mocker.patch.object(server, 'clubs', clubs_fixture['clubs'])
        mocker.patch.object(server, 'competitions',
                            competitions_fixture['competitions'])
        club = clubs_fixture['clubs'][0]
        initial_points = club['points']
        competition = competitions_fixture['competitions'][0]
        nb_of_places = 4
        data = {
            'club': club['name'], 'competition': competition['name'], 'places': nb_of_places}
        client.post('/purchasePlaces', data=data)
        updated_points = club['points']
        expected_points = int(initial_points) - nb_of_places

        assert updated_points == expected_points

    def test_book_past_competition_should_return_error_message(self, client, clubs_fixture, past_competitions_fixture, mocker):
        mocker.patch.object(server, 'competitions',
                            past_competitions_fixture)
        mocker.patch.object(server, 'clubs',
                            clubs_fixture)
        competition = [comp for comp in past_competitions_fixture['competitions']
                       if comp['name'] == 'Test past compet'][0]
        club = clubs_fixture['clubs'][0]
        data = {'club': club['name'], 'competitions': competition['name']}
        url = f"/book/{competition['name'].replace(' ', '%20')}/{club['name'].replace(' ', '%20')}"
        response = client.post(
            url, data=data)
        print('yoyoyo', response.data, competition, club)
        print(url)

        assert b'sorry, this competition allready took place' in response.data

    def test_book_future_competition_should_return_error_message(self, client, clubs_fixture, past_competitions_fixture, mocker):
        mocker.patch.object(server, 'competitions',
                            past_competitions_fixture)
        mocker.patch.object(server, 'clubs',
                            clubs_fixture)
        competition = [comp for comp in past_competitions_fixture['competitions']
                       if comp['name'] == 'Test future compet'][0]
        club = clubs_fixture['clubs'][0]
        data = {'club': club['name'], 'competitions': competition['name']}
        response = client.post(
            f"/book/{competition['name']}/{club['name']}", data=data)

        assert response.status_code == 200
        assert b'sorry, this competition allready took place' not in response.data
