from functools import partial
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from tasks.models import Task, Person
from tasks.serializers import TaskSerializer, PersonSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(detail=True, methods=['get', 'put'])
    def status(self, request, pk):
        try:
            task = Task.objects.filter(id=pk).get()
        except Task.DoesNotExist:
            return Response(f'A task with the id {pk} does not exist', status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            return Response({'status': task.status})
        else:
            serializer = TaskSerializer(task, data=request.data, partial=True)
            if serializer.is_valid():
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get', 'put'])
    def owner(self, request, pk):
        try:
            task = Task.objects.filter(id=pk).get()
        except Task.DoesNotExist:
            return Response(f'A task with the id {pk} does not exist', status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'GET':
            return Response(task.ownerId.id)
        else:
            serializer = TaskSerializer(task, data=request.data, partial=True)
            if serializer.is_valid():
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            return Response(headers={'Location':f'tasks/{task.id}', 'x-Created-Id':task.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer 

    @action(detail=True, methods=['get', 'post'])
    def tasks(self, request, pk):
        try:
            Person.objects.filter(id=pk).get()
        except Person.DoesNotExist:
            return Response(f'A person with the id {pk} does not exist', status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            person_tasks = Task.objects.filter(ownerId=pk)
            if person_tasks.count() < 1:
                return Response(data='Tasks do not exist', status=status.HTTP_404_NOT_FOUND)
            serializer = TaskSerializer(person_tasks, many=True)
            return Response(serializer.data)
        else:
            data = request.data.copy()
            data['ownerId'] = pk
            serializer = TaskSerializer(data=data)
            if serializer.is_valid():
                task = serializer.save()
                return Response(headers={'Location':f'tasks/{task.id}', 'x-Created-Id':task.id}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            person = serializer.save()
            return Response(headers={'Location':f'people/{person.id}', 'x-Created-Id':person.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
