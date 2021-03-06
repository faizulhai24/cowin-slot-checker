from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone


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
    last_notified_at = models.DateTimeField(null=True)

    def notified(self):
        self.last_notified_at = timezone.localtime()
        self.save()
#
# class District(models.Model):
#     district_cowin_id = models.IntegerField(db_index=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     last_synced_at = models.DateTimeField(db_index=True)
#     is_active = models.BooleanField(default=False)
#     high_priority = models.BooleanField(default=False)
