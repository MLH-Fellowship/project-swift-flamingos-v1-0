# tests/test_app.py

import unittest
import os

os.environ["TESTING"] = "true"
from app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert """<p class="h1">Mateo Martinez</p>""" in html

        # TODO Add more tests relating to the home page

        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert (
            """<p class="card-text">💻 Computer Science Student @ The University of Texas Rio Grande Valley 📱</p>"""
            in html
        )

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == len(json["timeline_posts"])
        # TODO Add more tests relating to the /api/timeline_post GET and POST apis
        # POST
        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "test",
                "email": "test@test.com",
                "content": "testing",
            },
        )
        assert response.status_code == 200

        # GET
        response = self.client.get("/api/timeline_post")
        data = response.get_data(as_text=True)
        # print(data)
        assert '"name":"test"' in data
        assert '"email":"test@test.com"' in data
        assert '"content":"testing"' in data

        # TODO Add more tests relating to the timeline page

    def test_malformed_timeline_post(self):

        # POST request missing name
        response = self.client.post(
            "/api/timeline_post",
            data={"email": "john@example.com", "content": "Hello World, I'm John"},
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post(
            "/api/timeline_post",
            data={"name": "John Doe", "email": "john@example.com", "content": ""},
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "email": "not-an-email",
                "content": "Hello world, I'm John!",
            },
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html
