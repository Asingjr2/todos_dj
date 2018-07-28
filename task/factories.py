import factory
import factory.fuzzy
from django.contrib.auth.models import User

from base.factories import BaseModelFactory

from .models import Task


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'user{}'.format(n))
    password = factory.fuzzy.FuzzyText(length=10)


class TaskFactory(BaseModelFactory):
    class Meta: 
        model = Task

    name = factory.fuzzy.FuzzyText(length=99)
    description = factory.fuzzy.FuzzyText(length=249)
    creator = factory.SubFactory(UserFactory)
