from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task(3)
    def summary(self):
        data = {'email': 'kate@shelifts.co.uk'}
        response = self.client.post('/showSummary', data=data)

    @task(3)
    def book(self):
        response = self.client.post(
            '/book/Spring%20Festival/Iron%20Temple')

    @task(3)
    def purchase(self):
        data = {'places': 3, 'club': 'Iron Temple',
                'competition': 'Spring Festival'}
        response = self.client.post('/purchasePlaces', data=data)

    @task(3)
    def board(self):
        response = self.client.get('/board')

    def on_start(self):
        response = self.client.get('/')
        return super().on_start()

    def on_stop(self):
        response = self.client.get('/logout')
        return super().on_stop()
