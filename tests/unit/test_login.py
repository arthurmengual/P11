import server
from server import app
from contextlib import contextmanager
from flask import template_rendered


@contextmanager
def captured_templates(app):
    '''This function captures the templates to further verify which one was rendered'''
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


class Testlogin:
    '''This is the classtest for the login and logout endpoints'''

    def test_login(self, client):
        '''This function tests the login enpoint and verify the status_code and template'''
        with captured_templates(app) as templates:
            response = client.get("/")
            assert response.status_code == 200
            assert len(templates) == 1
            template = templates[0]
            assert template.name == "index.html"

    def test_logout(self, client):
        '''This function tests the logout enpoint and verifies the status_code'''
        with captured_templates(app) as templates:
            response = client.get("/logout")
            assert response.status_code == 302
            assert len(templates) == 0

    def test_correct_email_should_return_200_status_code(
        self, client, clubs_fixture, mocker
    ):
        '''This function creates a client and tries to login with a correct email adress, then verifies
        the status_code and template rendered'''
        mocker.patch.object(server, "clubs", clubs_fixture["clubs"])
        email = clubs_fixture["clubs"][0]["email"]
        data = {"email": email}

        with captured_templates(app) as templates:
            response = client.post("/showSummary", data=data)
            assert response.status_code == 200
            assert len(templates) == 1
            template = templates[0]
            assert template.name == "welcome.html"

    def test_wrong_email_should_return_200_status_code(
        self, client, clubs_fixture, mocker
    ):
        '''This function creates a client and tries to login with a wrong email adress, then verifies
        the status_code and template rendered'''
        mocker.patch.object(server, "clubs", clubs_fixture["clubs"])
        email = "fake@fake.com"
        data = {"email": email}

        with captured_templates(app) as templates:
            response = app.test_client().post("/showSummary", data=data)
            assert response.status_code == 200
            assert b"<li>unknown email, try again</li>" in response.data
            assert len(templates) == 1
            template = templates[0]
            assert template.name == "index.html"
