from django.db import models
from django.contrib.auth.models import User


class MeetingCategories(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attendant = models.BooleanField()
    optional = models.BooleanField()
    event = models.ForeignKey('Meeting', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        if self.attendant:
            attendant_str = ''
        else:
            attendant_str = 'nicht'
        return f'{self.user}'


class Meeting(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    begin = models.TimeField()
    end = models.TimeField()
    category = models.ForeignKey('MeetingCategories', on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    participants = models.ManyToManyField(Participant, blank=True)

    def __str__(self):
        return self.name
