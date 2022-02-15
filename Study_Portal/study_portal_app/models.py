from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=199)

    def __str__(self):
        return self.title

class HomeWork(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=190)
    title = models.CharField(max_length=100)
    description= models.CharField(max_length=100)
    due = models.DateTimeField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    status =models.BooleanField(default=False)

    def __str__(self):
        return self.title
