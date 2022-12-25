from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    primary_identity = models.CharField(max_length=100)
    is_authenticated = models.BooleanField()
    tokens = models.CharField(max_length=10000, blank=True, null=True)