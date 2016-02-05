import json

import django.test

import ddgcorp.models


class WWWTests(django.test.TestCase):
    def setUp(self):
        self.client = django.test.Client()

    def test__get(self):
        resp = self.client.get('/')
        assert resp.status_code == 200

    def test__post(self):
        resp = self.client.post('/')
        # method not allowed
        assert resp.status_code == 405
