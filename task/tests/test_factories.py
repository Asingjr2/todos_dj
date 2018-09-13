from django.test import TestCase

import factory

from ..factories import TaskFactory


class TaskFactoryTestCase(TestCase):
    def test_factory(self):
        task = TaskFactory

        self.assertIsNotNone(task.name)
        self.assertIsNotNone(task.description)
        self.assertIsNotNone(task.creator)