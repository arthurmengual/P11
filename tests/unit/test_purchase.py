import pytest
import server


class Testpurchase:
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
