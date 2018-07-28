from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator, MinLengthValidator

from base.models import BaseModel


COMPLETED_STATUS = (
    ("NO", 'no'),
    ("YES", 'yes')
)


class Task(BaseModel):
    name = models.CharField(max_length=100, validators=[MaxLengthValidator(100, message='Must be less than 100 characters'), MinLengthValidator(5, message='Must be at least 5 characters')])
    description = models.CharField(max_length=250, validators=[MaxLengthValidator(250), MinLengthValidator(5, message='Must be at least 5 characters')])
    status = models.CharField(max_length=4, choices=COMPLETED_STATUS, default="NO")
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("task_detail", args=(self.id,)) 

