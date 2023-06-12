from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

# Create your models here.


class Login(AbstractUser):
    userType = models.CharField(max_length=100)
    viewPass = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.username


class School(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.IntegerField(max_length=100)
    address = models.CharField(max_length=300)
    state = models.CharField(max_length=100)
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Child(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.IntegerField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=100)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=300)
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    sender = models.ForeignKey(Child, on_delete=models.CASCADE)
    message = models.CharField(max_length=300)
    date = models.CharField(max_length=100, null=True)
    time = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=100)
