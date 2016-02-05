import datetime
import pytz

import django.db.models
import audit_log.models.managers

import ddgcorp.tools.enum


def get_max_audit_log_action_date(model):
    if not model.audit_log.count():
        # zero time
        return pytz.utc.localize(datetime.datetime.fromtimestamp(0))
    return model.audit_log.latest('action_date').action_date



class Status(django.db.models.Model):
    """
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
        #index=True,
    )

    audit_log = audit_log.models.managers.AuditLog()

    def __unicode__(self):
        return self.Enum(self.name)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.Enum(self.name),
        }


class Task(django.db.models.Model):
    """
    """

    name = django.db.models.CharField(
        max_length=100,
        blank=False,
    )
    status = django.db.models.ForeignKey(Status)

    def __unicode__(self):
        return '[{}] {} ({})'.format(
            self.id, self.name, str(self.status))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'status': self.status.to_dict(),
        }

    audit_log = audit_log.models.managers.AuditLog()
