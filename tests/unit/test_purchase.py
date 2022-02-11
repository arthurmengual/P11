import pytest
import server


class Testpurchase:
    def test_points_should_be_updated(self, client, clubs_fixture, competitions_fixture, mocker):
        mocker.patch.object(server, 'clubs', clubs_fixture['clubs'])
        mocker.patch.object(server, 'competitions',
                            competitions_fixture['competitions'])
        club = clubs_fixture['clubs'][0]
        competition = competitions_fixture['competitions'][0]
        nb_of_places = 4
        data = {'club': club, 'competition': competition, 'places': nb_of_places}
        client.post('/purchasePlaces', data=data)
        updated_points = club['points']
        expected_points = int(club['points']) - nb_of_places

        assert updated_points == expected_points
