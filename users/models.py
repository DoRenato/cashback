from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass


class Customer(models.Model):
    document = models.CharField(max_length=11, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
