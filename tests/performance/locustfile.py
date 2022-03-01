from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task
    def index(self):
        response = self.client.get('/')

    @task
    def summary(self):
        data = {'email': 'kate@shelifts.co.uk'}
        response = self.client.post('/showSummary', data=data)

    @task
    def book(self):
        response = self.client.post(
            '/book/Spring%20Festival/Iron%20Temple')

    @task
    def purchase(self):
        data = {'places': 3, 'club': 'Iron Temple',
                'competition': 'Spring Festival'}
        response = self.client.post('/purchasePlaces', data=data)

    @task
    def board(self):
        response = self.client.get('/board')

    def on_stop(self):
        response = self.client.get('/logout')
        return super().on_stop()
