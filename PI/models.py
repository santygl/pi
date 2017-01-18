from django.db import models
from django.contrib.auth.models import User


class Twitter(models.Model):
    secret = models.CharField(max_length=254, null=True, default=None)
    key = models.CharField(max_length=254, null=True, default=None)
    user = models.OneToOneField(User, related_name='twitter')


