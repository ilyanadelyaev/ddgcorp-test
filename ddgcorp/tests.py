import django.test
import django.db

import ddgcorp.models


class StatusModelTests(django.test.TestCase):
    """
    Model: Status
    """

    def test__blank(self):
        """
        blank=False
        """
        with self.assertRaises(django.db.IntegrityError) as ex_info:
            ddgcorp.models.Status(
                name=None,
            ).save()
        assert ex_info.exception.message == \
            'ddgcorp_status.name may not be NULL'

    def test__unique(self):
        """
        unique=True
        """
        ddgcorp.models.Status(
            name=ddgcorp.models.Status.Enum.new,
        ).save()
        # column name is not unique
        with self.assertRaises(django.db.IntegrityError) as ex_info:
            ddgcorp.models.Status(
                name=ddgcorp.models.Status.Enum.new,
            ).save()
        assert ex_info.exception.message == \
            'column name is not unique'

    def test__all(self):
        """
        all()
        """
        obj = ddgcorp.models.Status(
            name=ddgcorp.models.Status.Enum.new,
        )
        obj.save()
        #
        objs = ddgcorp.models.Status.all()
        #
        assert objs[0]['id'] == obj.id
        assert objs[0]['name'] == ddgcorp.models.Status.Enum(
            ddgcorp.models.Status.Enum.new)

    def test__to_dict(self):
        """
        to_dict()
        """
        obj = ddgcorp.models.Status(
            name=ddgcorp.models.Status.Enum.new,
        )
        obj.save()
        #
        dct = obj.to_dict()
        #
        assert dct['id'] == obj.id
        assert dct['name'] == ddgcorp.models.Status.Enum(
            ddgcorp.models.Status.Enum.new)


class TaskModelTests(django.test.TestCase):
    """
    Model: Task
    """

    def test__blank(self):
        """
        blank=False
        """
        status = ddgcorp.models.Status(
            name=ddgcorp.models.Status.Enum.new,
        )
        status.save()
        #
        with self.assertRaises(django.db.IntegrityError) as ex_info:
            ddgcorp.models.Task(
                name=None,
                status=status,
            ).save()
        assert ex_info.exception.message == \
            'ddgcorp_task.name may not be NULL'

    def test__one(self):
        """
        one
        """
        status = ddgcorp.models.Status(
            name=ddgcorp.models.Status.Enum.new,
        )
        status.save()
        task = ddgcorp.models.Task(
            name='name',
            status=status,
        )
        task.save()
        #
        obj = ddgcorp.models.Task.one(task.pk)
        #
        assert obj['id'] == task.id
        assert obj['name'] == task.name
        assert obj['status_id'] == status.id

    def test__one__none(self):
        """
        one() returns None
        """
        obj = ddgcorp.models.Task.one(0)
        assert obj is None

    def test__all(self):
        """
        all()
        """
        status = ddgcorp.models.Status(
            name=ddgcorp.models.Status.Enum.new,
        )
        status.save()
        task = ddgcorp.models.Task(
            name='name',
            status=status,
        )
        task.save()
        #
        objs = ddgcorp.models.Task.all()
        #
        assert objs[0]['id'] == task.id
        assert objs[0]['name'] == task.name
        assert objs[0]['status_id'] == status.id

    def test__all__empty(self):
        """
        all() returns []
        """
        objs = ddgcorp.models.Task.all()
        assert objs == []

    def test__update_status(self):
        """
        update_status()
        """
        status_1 = ddgcorp.models.Status(
            name=ddgcorp.models.Status.Enum.new,
        )
        status_1.save()
        status_2 = ddgcorp.models.Status(
            name=ddgcorp.models.Status.Enum.tested,
        )
        status_2.save()
        task = ddgcorp.models.Task(
            name='name',
            status=status_1,
        )
        task.save()
        #
        ddgcorp.models.Task.update_status(task.id, status_2.id)
        #
        obj = ddgcorp.models.Task.one(task.id)
        assert obj['status_id'] == status_2.id

    def test__update_status__invalid_task(self):
        """
        update_status() raises TaskModelException
        """
        with self.assertRaises(
                ddgcorp.models.TaskModelException) as ex_info:
            ddgcorp.models.Task.update_status(0, 0)
        assert ex_info.exception.message == \
            'Task 0 does not exist'

    def test__update_status__invalid_status(self):
        """
        update_status() raises TaskModelException
        """
        status = ddgcorp.models.Status(
            name=ddgcorp.models.Status.Enum.new,
        )
        status.save()
        task = ddgcorp.models.Task(
            name='name',
            status=status,
        )
        task.save()
        #
        with self.assertRaises(
                ddgcorp.models.TaskModelException) as ex_info:
            ddgcorp.models.Task.update_status(task.id, 0)
        assert ex_info.exception.message == \
            'Status 0 does not exist'

    def test__to_dict(self):
        """
        to_dict()
        """
        status = ddgcorp.models.Status(
            name=ddgcorp.models.Status.Enum.new,
        )
        task = ddgcorp.models.Task(
            name='name',
            status=status,
        )
        dct = task.to_dict()
        #
        assert dct['id'] == task.id
        assert dct['name'] == 'name'
        assert dct['status_id'] == status.id
