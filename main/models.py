from django.contrib.auth.models import User
from django.db import models


class Subjects(models.Model):
    name = models.CharField(max_length=32)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teaches')
    students = models.ManyToManyField(User, related_name='learns')


class Grades(models.Model):
    value = models.IntegerField()
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    graded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='graded')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grades')


class Messages(models.Model):
    send_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='msg_send')
    send_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='msg_received')
    title = models.CharField(max_length=32)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
