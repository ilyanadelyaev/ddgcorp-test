import django.test
import django.db

import ddgcorp.models


class StatusModelTests(django.test.TestCase):
    def test__unique(self):
        ddgcorp.models.Status(
            name=ddgcorp.models.Status.Enum.new,
        ).save()
        # column name is not unique
        with self.assertRaises(django.db.IntegrityError) as ex_info:
            ddgcorp.models.Status(
                name=ddgcorp.models.Status.Enum.new,
            ).save()
        self.assertEqual(
            ex_info.exception.message,
            'column name is not unique'
        )
