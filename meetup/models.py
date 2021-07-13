import uuid

from django.contrib.auth import get_user_model
from django.db import models


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
    attendant = models.BooleanField()
    optional = models.BooleanField()

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
