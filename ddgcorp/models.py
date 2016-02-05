import datetime
import pytz
import calendar

import django.db.models
import audit_log.models.managers

import ddgcorp.tools.enum


class Audit(object):
    """
    Mixin processor audit_log in models
    """

    @classmethod
    def get_last_modify_timestamp(cls):
        """
        Returns zero date in not exists
        """
        if not cls.audit_log.count():
            return 0
        date = cls.audit_log.latest('action_date').action_date
        return calendar.timegm(date.timetuple())


class Status(django.db.models.Model, Audit):
    """
    Task status
    """

    class Enum(ddgcorp.tools.enum.Enum):
        new = 0
        in_progress = 1
        on_review = 2
        tested = 3
        delivered = 4

        choices = (
            (new, 'New'),
            (in_progress, 'InProgress'),
            (on_review, 'OnReview'),
            (tested, 'Tested'),
            (delivered, 'Delivered'),
        )

    name = django.db.models.PositiveSmallIntegerField(
        choices=Enum.choices,
        unique=True,
        blank=False,
    )

    audit_log = audit_log.models.managers.AuditLog()

    def __unicode__(self):
        return self.Enum(self.name)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.Enum(self.name),
        }


class Task(django.db.models.Model, Audit):
    """
    Task info
    """

    name = django.db.models.CharField(
        max_length=100,
        blank=False,
    )
    status = django.db.models.ForeignKey(Status)

    audit_log = audit_log.models.managers.AuditLog()

    def __unicode__(self):
        return '[{}] {} ({})'.format(
            self.id, self.name, str(self.status))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'status': self.status.to_dict(),
        }
