from django.test import Client, TestCase
from django.urls import reverse

import factory
from ..factories import TaskFactory, UserFactory


class TaskHomeViewTestCase(TestCase):
    def test_200(self):
        client = Client()
        logged_user = UserFactory()
        client.force_login(logged_user)
        response = client.get("/home")
        self.assertEqual(response.status_code, 200)

    def test_302(self):
        client = Client()
        response = client.get("/home")
        self.assertEqual(response.status_code, 302)


class TaskListViewTestCase(TestCase):
    def test_200(self):
        client = Client()
        logged_user = UserFactory()
        client.force_login(logged_user)
        response = client.get("/all_tasks")
        self.assertEqual(response.status_code, 200)

    def test_302(self):
        client = Client()
        response = client.get("/all_tasks")
        self.assertEqual(response.status_code, 302)


# Does not work
class TaskCreateViewTestCase(TestCase):
    def test_200(self):
        url = reverse("task_create")
        logged_user = UserFactory()
        
        client = Client()
        client.force_login(logged_user)
        response = client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_302(self):
        url = reverse("task_create")
        data = {}

        client = Client()
        response = client.post(url, data)
        self.assertEqual(response.status_code, 302)


#  Does not work
class TaskDetailViewTestCase(TestCase):
    def test_200(self):
        task = TaskFactory()
        logged_user = UserFactory()
        url = task.get_absolute_url()

        client = Client()
        client.force_login(logged_user)
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_302(self):
        task = TaskFactory()
        url = task.get_absolute_url()

        client = Client()
        response = client.post(url)
        self.assertEqual(response.status_code, 302)


class TaskUpdateViewTestCase(TestCase):
    def test_200(self):
        task = TaskFactory()
        logged_user = UserFactory()
        url = reverse("task_update", args=(task.id,))
        data = {"name":"new name"}

        client = Client()
        client.force_login(logged_user)
        response = client.post(url, data)
        self.assertEqual(response.status_code, 200 )

    def test_302(self):
        task = TaskFactory()
        url = reverse("task_update", args=(task.id,))
        data = {"name":"new name"}

        client = Client()
        response = client.post(url, data)
        self.assertEqual(response.status_code, 302 )


# Does not work
class TaskDeleteViewTestCase(TestCase):
    def test_200(self):
        task = TaskFactory()
        logged_user = UserFactory()
        url = reverse("task_delete", args=(task.id,))

        client = Client()
        client.force_login(logged_user)
        response = client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_302(self):
        task = TaskFactory()
        url = reverse("task_delete", args=(task.id,))

        client = Client()
        response = client.post(url)
        self.assertEqual(response.status_code, 302)



