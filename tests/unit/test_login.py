import server
from server import app
from flask import template_rendered
from contextlib import contextmanager
from flask import template_rendered


@contextmanager
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


class Testlogin:
    def test_login(self, client):
        with captured_templates(app) as templates:
            rv = app.test_client().get('/')
            assert rv.status_code == 200
            assert len(templates) == 1
            template, context = templates[0]
            assert template.name == 'index.html'

    def test_logout(self, client):
        with captured_templates(app) as templates:
            rv = app.test_client().get('/logout')
            assert rv.status_code == 302
            # checker template

    def test_correct_email_should_return_200_status_code(self, client, clubs_fixture, mocker):
        mocker.patch.object(server, 'clubs', clubs_fixture['clubs'])
        email = clubs_fixture['clubs'][0]['email']
        data = {'email': email}
        response = client.post('/showSummary', data=data)

        assert response.status_code == 200

        with captured_templates(app) as templates:
            rv = app.test_client().post('/showSummary', data=data)
            assert rv.status_code == 200
            assert len(templates) == 1
            template, context = templates[0]
            assert template.name == 'welcome.html'

    def test_wrong_email_should_return_200_status_code(self, client, clubs_fixture, mocker):
        mocker.patch.object(server, 'clubs', clubs_fixture['clubs'])
        email = 'fake@fake.com'
        data = {'email': email}
        response = client.post('/showSummary', data=data)

        assert b"<li>unknown email, try again</li>" in response.data

        with captured_templates(app) as templates:
            rv = app.test_client().post('/showSummary', data=data)
            assert rv.status_code == 200
            assert len(templates) == 1
            template, context = templates[0]
            assert template.name == 'index.html'
