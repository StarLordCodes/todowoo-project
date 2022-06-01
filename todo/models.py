from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    title = models.CharField(max_length=200)
    # allows to add model even without content in memo
    memo = models.TextField(blank=True)
    # automatically add created date and time
    created = models.DateTimeField(auto_now_add=True)
    # allows to create objects even if datecompleted is not filled
    datecompleted = models.DateTimeField(blank=True, null=True)
    # set important as False for default
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
