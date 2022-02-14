import pytest
import server


class Testpurchase:
    def test_more_than_12_points_should_return_error_message(self, client, clubs_fixture, competitions_fixture, mocker):
        mocker.patch.object(server, 'clubs', clubs_fixture['clubs'])
        mocker.patch.object(server, 'competitions',
                            competitions_fixture['competitions'])
        club = clubs_fixture['clubs'][0]
        competition = competitions_fixture['competitions'][0]
        data = {'places': 13, 'club': club['name'],
                'competition': competition['name']}
        response = client.post('/purchasePlaces', data=data)
        print(response.data)

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
