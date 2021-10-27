from django.db import models

# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=1000)
    details = models.CharField(max_length=1000)
    dueDate = models.DateField()
    status = models.CharField(max_length=100, choices=[
        ('active', 'active'),
        ('done', 'done'),
    ])
    ownerId = models.ForeignKey('Person', on_delete=models.CASCADE)

class Person(models.Model):
    name = models.CharField(max_length=1000)
    email = models.EmailField(unique=True)
    favoriteProgrammingLanguage = models.CharField(max_length=1000)
    activeTaskCount = models.IntegerField()
