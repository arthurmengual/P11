import server
from server import app
from flask import template_rendered
from contextlib import contextmanager
from flask import template_rendered


@contextmanager
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


class Testlogin:
    def test_login(self, client):
        with captured_templates(app) as templates:
            response = client.get('/')
            assert response.status_code == 200
            assert len(templates) == 1
            template = templates[0]
            assert template.name == 'index.html'

    def test_logout(self, client):
        with captured_templates(app) as templates:
            response = client.get('/logout')
            assert response.status_code == 302
            # checker template

    def test_correct_email_should_return_200_status_code(self, client, clubs_fixture, mocker):
        mocker.patch.object(server, 'clubs', clubs_fixture['clubs'])
        email = clubs_fixture['clubs'][0]['email']
        data = {'email': email}

        with captured_templates(app) as templates:
            response = client.post('/showSummary', data=data)
            assert response.status_code == 200
            assert len(templates) == 1
            template = templates[0]
            assert template.name == 'welcome.html'

    def test_wrong_email_should_return_200_status_code(self, client, clubs_fixture, mocker):
        mocker.patch.object(server, 'clubs', clubs_fixture['clubs'])
        email = 'fake@fake.com'
        data = {'email': email}

        with captured_templates(app) as templates:
            response = app.test_client().post('/showSummary', data=data)
            assert response.status_code == 200
            assert b"<li>unknown email, try again</li>" in response.data
            assert len(templates) == 1
            template = templates[0]
            assert template.name == 'index.html'
