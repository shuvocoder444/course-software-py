import uuid

from django.db import models


class InstituteSetting(models.Model):
    website_name = models.CharField(max_length=255, default="My Institute Portal Layout")
    send_id_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.website_name
