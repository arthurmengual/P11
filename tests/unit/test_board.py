from server import app
from flask import template_rendered
from contextlib import contextmanager


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


class TestBoard:
    def test(self, client):

        with captured_templates(app) as templates:
            response = client.get('/board')
            assert response.status_code == 200
            assert b'Points board' in response.data
            assert len(templates) == 1
            template = templates[0]
            assert template.name == 'board.html'
