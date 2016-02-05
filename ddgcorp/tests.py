import time

import django.test
import django.db

import ddgcorp.models


class AuditTests(django.test.TestCase):
    def test__last_modify(self):
        """
        correct timestamp
        """
        start_time = time.time()
        ddgcorp.models.Status(
            name=ddgcorp.models.Status.Enum.new,
        ).save()
        end_time = time.time()
        #
        modify = ddgcorp.models.Status.get_last_modify_timestamp()
        assert modify >= int(start_time) and modify <= int(end_time)


class StatusModelTests(django.test.TestCase):
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
        obj = ddgcorp.models.Status(
            name=ddgcorp.models.Status.Enum.new,
        )
        dct = obj.to_dict()
        #
        assert dct['id'] == obj.id
        assert dct['name'] == ddgcorp.models.Status.Enum(
            ddgcorp.models.Status.Enum.new)


class TaskModelTests(django.test.TestCase):
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
