from rest_framework import serializers

from tasks.models import Task, Person

class TaskSerizlier(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'
