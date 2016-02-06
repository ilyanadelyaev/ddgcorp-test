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

    def test__to_dict(self):
        """
        to_dict()
        """
        obj = ddgcorp.models.Status(
            name=ddgcorp.models.Status.Enum.new,
        )
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
        assert dct['status']['id'] == status.id
