import django.db.models

import ddgcorp.tools.enum


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
        return '[{}] {}'.format(self.id, self.name)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'status': self.status.to_dict(),
        }
