from server import app
from flask import template_rendered
from contextlib import contextmanager


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


class TestBoard:
    '''This is the testclass for the points board'''

    def test(self, client):
        '''This test creates a client send a request on the points board and verify
        the status_code et the template rendered'''

        with captured_templates(app) as templates:
            response = client.get("/board")
            assert response.status_code == 200
            assert b"Points board" in response.data
            assert len(templates) == 1
            template = templates[0]
            assert template.name == "board.html"
