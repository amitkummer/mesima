from rest_framework import serializers

from tasks.models import Task, Person

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['name', 'email', 'favoriteProgrammingLanguage', 'activeTaskCount']