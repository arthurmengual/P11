import pytest
import server


class Testpurchase:
    def more_thant_club_points_should_return_error_message(self, client, clubs_fixture, mocker):
        club_test = clubs_fixture['clubs'][0]
        mocker.patch.object(server.purchasePlaces, 'club', club_test)
        data = {'places': int(club_test['ponts']+1)}
        response = client.post('/purchasePlaces', data=data)

        assert b'sorry, you do not have enough points' in response.data
