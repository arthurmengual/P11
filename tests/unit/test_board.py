from server import app
from flask import template_rendered
from contextlib import contextmanager


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


class TestBoard:
    def test(self, client):
        response = client.get('/board')

        assert b'Points board' in response.data

        with captured_templates(app) as templates:
            rv = app.test_client().get('/board')
            assert rv.status_code == 200
            assert len(templates) == 1
            template, context = templates[0]
            assert template.name == 'board.html'
