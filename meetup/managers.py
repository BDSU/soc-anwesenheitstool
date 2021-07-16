from django.db import models
from django.db.models import QuerySet


class EmptyManager(models.Manager):
    """
    Manager that always returns an empty QuerySet

    Used to create virtual models, that can be saved in the admin
    """
    def get_queryset(self):
        return QuerySet(self.model).none()