import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models

from meetup.managers import EmptyManager


class MeetingCategories(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Meeting Categories"
        verbose_name = "Meeting Category"

    def __str__(self):
        return self.name


class Participant(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    meeting = models.ForeignKey('Meeting', on_delete=models.CASCADE)
    attendant = models.BooleanField(default=False)
    optional = models.BooleanField()

    allow_excuse = models.BooleanField(default=False)
    excused = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'meeting')

    def __str__(self):
        return f'{self.user}'


class Meeting(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    begin = models.TimeField()
    end = models.TimeField()
    category = models.ForeignKey('MeetingCategories', on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)

    participants = models.ManyToManyField(get_user_model(), blank=True, through=Participant)

    presence_registration_uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.name


class GroupParticipants(models.Model):
    """
    Used for creating Participant-instances for whole groups
    """
    meeting = models.ForeignKey(Meeting, null=False, on_delete=models.DO_NOTHING)
    group = models.ForeignKey(Group, null=False, on_delete=models.DO_NOTHING)
    objects = EmptyManager()
    optional = models.BooleanField()

    allow_excuse = models.BooleanField(default=False)

    class Meta:
        managed = False
        verbose_name = "Group Participants"
        verbose_name_plural = "Group Participants"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # If a user is already a participant, do not create another Participant instance for them
        create_for_users = self.group.user_set.exclude(
            pk__in=self.meeting.participants.values_list("pk")
        )

        Participant.objects.bulk_create(
            [
                Participant(
                    user=user,
                    meeting=self.meeting,
                    optional=self.optional,
                    allow_excuse=self.allow_excuse,
                )
                for user in create_for_users
            ]
        )
