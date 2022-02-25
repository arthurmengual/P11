from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task(3)
    def login(self, clubs_fixture):
        club = clubs_fixture['clubs'][0]
        data = {'email': club['email']}
        self.client.post('/login', data=data)
