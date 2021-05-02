from django.db import models
from django.contrib.postgres.fields import ArrayField


class User(models.Model):
    phone_number = models.CharField(max_length=15, blank=False, unique=True)
    first_name = models.CharField(max_length=255, blank=False, default='')
    state_id = models.IntegerField()
    district_ids = ArrayField(models.IntegerField(), null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    verified = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    message_consent = models.BooleanField(default=False)

