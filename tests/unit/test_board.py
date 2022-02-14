import pytest
import server


class Testboard:
    def test(self, client):
        response = client.get('/board')

        assert b'Points board' in response.data
