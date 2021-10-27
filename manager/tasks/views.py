from django.shortcuts import render
from rest_framework import viewsets

from tasks.models import Task, Person
from tasks.serializers import TaskSerizlier, PersonSerializer

# Create your views here.

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerizlier

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer 
