from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    '''This is the class for the performance tests of the app'''
    @task
    def index(self):
        '''This is the test for the index enpoint'''
        response = self.client.get("/")

    @task
    def summary(self):
        '''This is the test for the summary enpoint'''
        data = {"email": "kate@shelifts.co.uk"}
        response = self.client.post("/showSummary", data=data)

    @task
    def book(self):
        '''This is the test for the booking enpoint'''
        response = self.client.post("/book/Spring%20Festival/Iron%20Temple")

    @task
    def purchase(self):
        '''This is the test for the purchase enpoint'''
        data = {"places": 3, "club": "Iron Temple", "competition": "Spring Festival"}
        response = self.client.post("/purchasePlaces", data=data)

    @task
    def board(self):
        '''This is the test for the board display enpoint'''
        response = self.client.get("/board")

    def on_stop(self):
        '''This is the test for the logout enpoint'''
        response = self.client.get("/logout")
        return super().on_stop()
