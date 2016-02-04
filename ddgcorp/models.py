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
        blank=True,
        #index=True,
    )

    def __unicode__(self):
        return self.Enum(self.name)
