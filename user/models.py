from django.db import models


# Create your models here.
class User(models.Model):
    email = models.EmailField(max_length=20, primary_key=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    sex = models.CharField(max_length=5, default='秘密')
    author_id = models.CharField(max_length=25, default=None)


def application_path(instance, filename):
    return 'attachment/user_{0}/{1}'.format(instance.user.email, filename)


class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author_id = models.CharField(max_length=25)
    author_name = models.CharField(max_length=50)
    description = models.TextField()
    attachment = models.FileField(upload_to=application_path)


