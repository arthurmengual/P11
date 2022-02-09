import pytest
import server


class Testpurchase:
    def test_more_than_12_points_shoul_return_error_message(self, client, clubs_fixture, competitions_fixture, mocker):
        mocker.patch.object(server, 'clubs', clubs_fixture['clubs'])
        mocker.patch.object(server, 'competitions',
                            competitions_fixture['competitions'])
        club = clubs_fixture['clubs'][0]
        competition = competitions_fixture['competitions'][0]
        places = 13
        data = {'club': club, 'competition': competition, 'places': places}
        response = client.post('/purchasePlaces', data=data)

        assert b'sorry, you cannot purchase more that 12 places' in response.data
