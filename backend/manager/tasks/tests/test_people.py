import json
from datetime import date

from django.urls import reverse
from rest_framework.test import APITestCase
from tasks.models import Person

from tasks.models import Task, Person


class PersonListTests(APITestCase):
    def setUp(self):
        self.person = Person(
            name="Amit", email="amit@amit.com", favoriteProgrammingLanguage="scala"
        )
        self.person.save()
        self.another_person = Person(
            name="Amit",
            email="amit_other@amit.com",
            favoriteProgrammingLanguage="scala",
        )
        self.another_person.save()
        self.task = Task(
            title="task",
            details="details",
            dueDate=date.today(),
            status="active",
            ownerId=self.person,
        )
        self.task.save()
        self.another_task = Task(
            title="another task",
            details="another details",
            dueDate=date.today(),
            status="done",
            ownerId=self.person,
        )
        self.another_task.save()

    def test_get(self):
        response = self.client.get(reverse("person-list"))
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 2)  # Multiple persons

        self.assertContains(response, "name")
        self.assertContains(response, "email")
        self.assertContains(response, "favoriteProgrammingLanguage")
        self.assertContains(response, "activeTaskCount")

    def test_post(self):
        response = self.client.post(
            reverse("person-list"),
            data={
                "name": "Ido",
                "email": "ido@gmail.com",
                "favoriteProgrammingLanguage": "Python",
            },
        )
        self.assertEqual(response.status_code, 201)
        id = Person.objects.filter(name="Ido").get().id
        self.assertEqual(response.headers["Location"], f"people/{id}")
        self.assertEqual(response.headers["x-Created-Id"], str(id))

    def test_post_400(self):
        response = self.client.post(
            reverse("person-list"),
            data={"email": "ido@gmail.com", "favoriteProgrammingLanguage": "Python"},
        )
        self.assertEqual(response.status_code, 400)


class PersonDetailTests(APITestCase):
    def setUp(self):
        self.person = Person(
            name="Amit", email="amit@amit.com", favoriteProgrammingLanguage="scala"
        )
        self.person.save()
        self.another_person = Person(
            name="Amit",
            email="amit_other@amit.com",
            favoriteProgrammingLanguage="scala",
        )
        self.another_person.save()
        self.task = Task(
            title="task",
            details="details",
            dueDate=date.today(),
            status="active",
            ownerId=self.person,
        )
        self.task.save()
        self.another_task = Task(
            title="another task",
            details="another details",
            dueDate=date.today(),
            status="done",
            ownerId=self.person,
        )
        self.another_task.save()

    def test_get(self):
        response = self.client.get(reverse("person-detail", args=[self.person.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "name")
        self.assertContains(response, "email")
        self.assertContains(response, "favoriteProgrammingLanguage")
        self.assertContains(response, "activeTaskCount")

    def test_patch(self):
        response = self.client.patch(
            reverse("person-detail", args=[self.person.id]),
            data={"name": "new name", "email": "new@gmail.com"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "new name")
        self.assertEqual(response.data["email"], "new@gmail.com")

    def test_delete(self):
        response = self.client.delete(reverse("person-detail", args=[self.person.id]))
        self.assertEqual(response.status_code, 200)

    def test_get_tasks_nested(self):
        response = self.client.get(reverse("person-tasks", args=[self.person.id]))
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 2)  # Multiple persons

        self.assertContains(response, "title")
        self.assertContains(response, "details")
        self.assertContains(response, "dueDate")
        self.assertContains(response, "status")
        self.assertContains(response, "ownerId")

    def test_get_tasks_nested_get_params_active(self):
        response = self.client.get(
            reverse("person-tasks", args=[self.person.id]) + "?status=active"
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)  # Multiple persons

        self.assertEqual(content[0]["status"], "active")

    def test_get_tasks_nested_get_params_done(self):
        response = self.client.get(
            reverse("person-tasks", args=[self.person.id]) + "?status=done"
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)  # Multiple persons

        self.assertEqual(content[0]["status"], "done")

    def test_get_tasks_nested_404(self):
        response = self.client.get(reverse("person-tasks", args=[1337]))
        self.assertEqual(response.status_code, 404)

    def test_post_tasks_nested(self):
        response = self.client.post(
            reverse("person-tasks", args=[self.person.id]),
            data={
                "title": "a tour of c++",
                "details": "details",
                "dueDate": date.today(),
                "status": "active",
            },
        )
        self.assertEqual(response.status_code, 201)
        id = Task.objects.filter(title="a tour of c++").get().id
        self.assertEqual(response.headers["Location"], f"tasks/{id}")
        self.assertEqual(response.headers["x-Created-Id"], str(id))

    def test_post_tasks_nested_400(self):
        response = self.client.post(
            reverse("person-tasks", args=[self.person.id]),
            data={"details": "details", "dueDate": date.today(), "status": "active"},
        )
        self.assertEqual(response.status_code, 400)

    def test_post_tasks_nested_404(self):
        response = self.client.post(
            reverse("person-tasks", args=[1337]),
            data={
                "title": "a tour of c++",
                "details": "details",
                "dueDate": date.today().isoformat(),
                "status": "active",
            },
        )
        self.assertEqual(response.status_code, 404)
