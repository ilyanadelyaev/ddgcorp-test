import json

import django.test

import ddgcorp.models


class APITests(django.test.TestCase):
    def setUp(self):
        self.client = django.test.Client()
        # create statuses
        for s in ddgcorp.models.Status.Enum:
            ddgcorp.models.Status(name=s).save()
        # create tasks
        ddgcorp.models.Task(
            name='JS',
            status=ddgcorp.models.Status.objects.get(
                name=ddgcorp.models.Status.Enum.new
            ),
        ).save()

    def test__tasks(self):
        resp = self.client.get(
            '/api/task/',
        )
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(len(data), 1)
