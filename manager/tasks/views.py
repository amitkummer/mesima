from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from tasks.models import Task, Person
from tasks.serializers import TaskSerializer, PersonSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer 

    @action(detail=True, methods=['get', 'post'])
    def tasks(self, request, pk):
        if request.method == 'GET':
            person_tasks = Task.objects.filter(ownerId=pk)
            if person_tasks.count() < 1:
                return Response(data="{'Tasks not found'}", status=status.HTTP_404_NOT_FOUND)
            serializer = TaskSerializer(person_tasks, many=True)
            return Response(serializer.data)
        else:
            serializer = TaskSerializer(data=request.data)
            if serializer.is_valid():
                task = Task(serializer.data)
                task.save()
                return Response({'status': 'created'})
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
