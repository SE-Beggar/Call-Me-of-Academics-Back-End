from django.db import models


# Create your models here.
class User(models.Model):
    email = models.EmailField(max_length=20, primary_key=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    sex = models.CharField(max_length=5)