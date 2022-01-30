from django.db import models

# Create your models here.
# https://docs.djangoproject.com/en/4.0/ref/models/fields/


class Task(models.Model):
    title = models.CharField(max_length=1000)
    details = models.CharField(max_length=1000)
    dueDate = models.DateField()
    status = models.CharField(
        max_length=100,
        choices=[
            ("active", "active"),
            ("done", "done"),
        ],
    )
    ownerId = models.ForeignKey("Person", on_delete=models.CASCADE)


class Person(models.Model):
    name = models.CharField(max_length=1000)
    email = models.EmailField(unique=True)
    favoriteProgrammingLanguage = models.CharField(max_length=1000)

    # Computed property (field) for a person's task count.
    # https://docs.djangoproject.com/en/4.0/topics/db/models/#model-methods
    @property
    def activeTaskCount(self):
        return Task.objects.filter(ownerId=self.id).count()
