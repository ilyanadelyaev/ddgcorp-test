import json

import django.test

import ddgcorp.models


class RESTTests(django.test.TestCase):
    """
    REST methods tests
    """

    def setUp(self):
        self.client = django.test.Client()

    def test__statuses__get(self):
        status = ddgcorp.models.Status(
            name=ddgcorp.models.Status.Enum.new,
        )
        status.save()
        #
        resp = self.client.get(
            '/api/status/',
        )
        assert resp.status_code == 200
        assert resp.json() == [{
            'id': status.id,
            'name': ddgcorp.models.Status.Enum(status.name),
        }]

    def test__statuses__post(self):
        resp = self.client.post('/api/status/')
        # method not allowed
        assert resp.status_code == 405

    def test__tasks__get(self):
        status = ddgcorp.models.Status(
            name=ddgcorp.models.Status.Enum.new,
        )
        status.save()
        task = ddgcorp.models.Task(
            name='task-name',
            status=status,
        )
        task.save()
        #
        resp = self.client.get(
            '/api/task/',
        )
        assert resp.status_code == 200
        assert resp.json() == [{
            'id': task.id,
            'name': task.name,
            'status_id': status.id,
        }]

    def test__tasks__post(self):
        resp = self.client.post('/api/task/')
        # method not allowed
        assert resp.status_code == 405

    def test__task__get(self):
        status = ddgcorp.models.Status(
            name=ddgcorp.models.Status.Enum.new,
        )
        status.save()
        task = ddgcorp.models.Task(
            name='task-name',
            status=status,
        )
        task.save()
        #
        resp = self.client.get(
            '/api/task/{}/'.format(task.id),
        )
        assert resp.status_code == 200
        assert resp.json() == {
            'id': task.id,
            'name': task.name,
            'status_id': status.id,
        }

    def test__task__get__not_exists(self):
        resp = self.client.get(
            '/api/task/0/',
        )
        assert resp.status_code == 404

    def test__task_status__put(self):
        status_new = ddgcorp.models.Status(
            name=ddgcorp.models.Status.Enum.new,
        )
        status_new.save()
        status_tested = ddgcorp.models.Status(
            name=ddgcorp.models.Status.Enum.tested,
        )
        status_tested.save()
        task = ddgcorp.models.Task(
            name='task-name',
            status=status_new,
        )
        task.save()
        #
        resp = self.client.put(
            '/api/task/{}/status/'.format(task.id),
            data=json.dumps({
                'status': status_tested.id,
            }),
            content_type='application/json',
        )
        assert resp.status_code == 200
        # status updated
        task = ddgcorp.models.Task.objects.filter(pk=task.id).first()
        assert task.status.name == ddgcorp.models.Status.Enum.tested

    def test__task__status__put__invalid_data(self):
        resp = self.client.put(
            '/api/task/0/status/',
            data=json.dumps({
            }),
            content_type='application/json',
        )
        # status not in data
        assert resp.status_code == 404

    def test__task__status__put__task_not_exists(self):
        resp = self.client.put(
            '/api/task/0/status/',
            data=json.dumps({
                'status': 0,
            }),
            content_type='application/json',
        )
        assert resp.status_code == 404

    def test__task__status__put__status_not_exists(self):
        status = ddgcorp.models.Status(
            name=ddgcorp.models.Status.Enum.new,
        )
        status.save()
        task = ddgcorp.models.Task(
            name='task-name',
            status=status,
        )
        task.save()
        #
        resp = self.client.put(
            '/api/task/{}/status/'.format(task.id),
            data=json.dumps({
                'status': 1000,
            }),
            content_type='application/json',
        )
        # status not exists
        assert resp.status_code == 404

    def test__task__status__get(self):
        resp = self.client.post('/api/task/1/status/')
        # method not allowed
        assert resp.status_code == 405
