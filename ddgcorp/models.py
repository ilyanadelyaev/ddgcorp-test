import django.db.models

import ddgcorp.tools.enum


class ModelsError(Exception):
    """
    Unknown models error
    """


class TaskModelError(ModelsError):
    """
    Task model error
    """


class Status(django.db.models.Model):
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

    def __unicode__(self):
        return self.Enum(self.name)

    @classmethod
    def all(cls):
        """
        Get all list
        """
        return [
            {'id': o['id'], 'name': cls.Enum(o['name'])}
            for o in cls.objects.values('id', 'name').all()
        ]

    def to_dict(self):
        """
        Obfuscation
        """
        return {
            'id': self.id,
            'name': self.Enum(self.name),
        }


class Task(django.db.models.Model):
    """
    Task info
    """

    name = django.db.models.CharField(
        max_length=100,
        blank=False,
    )
    status = django.db.models.ForeignKey(Status)

    def __unicode__(self):
        return '[{}] {} ({})'.format(
            self.id, self.name, str(self.status))

    @classmethod
    def one(cls, pk):
        """
        Get one or none
        """
        return cls.objects.filter(pk=pk).values(
            'id', 'name', 'status_id').first()

    @classmethod
    def all(cls):
        """
        Get all list
        """
        return list(cls.objects.values('id', 'name', 'status_id').all())

    @classmethod
    def update_status(cls, pk, status_id):
        """
        Update task status
        """
        # Use TRANSACTION here
        task = cls.objects.filter(pk=pk).first()
        if not task:
            raise TaskModelError(
                'Task {} does not exist'.format(pk))
        status = Status.objects.filter(pk=status_id).first()
        if not status:
            raise TaskModelError(
                'Status {} does not exist'.format(status_id))
        # update status
        task.status = status
        task.save()

    def to_dict(self):
        """
        Obfuscation
        """
        return {
            'id': self.id,
            'name': self.name,
            'status_id': self.status.id,
        }
