from django.db import models
from django.contrib.auth.models import User


class Summary(models.Model):
    name = models.CharField(max_length=100, null=True)
    inputData = models.TextField(null=True, blank=True)
    outputData = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datecompleted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

