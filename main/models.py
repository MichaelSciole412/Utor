from django.db import models
from django.contrib.auth.models import AbstractUser
import json

class University(models.Model):
    name = models.CharField(max_length=150)
    domains = models.TextField(null=True)
    web_pages = models.TextField(null=True)
    country = models.CharField(max_length=50)
    alpha_two_code = models.CharField(max_length=10)
    state_province = models.CharField(max_length=100)


class User(AbstractUser):
    tutor_subjects = models.TextField(null=True)
    university = models.ForeignKey(University, on_delete=models.PROTECT, null=True, blank=True)
    bio = models.TextField(default="This user hasn't set their bio")

    def get_tutor_subjects(self):
        return json.loads(self.tutor_subjects or "[]")
    def set_tutor_subjects(self, subjects):
        self.tutor_subjects = json.dumps(subjects)
        self.save()
    def add_tutor_subject(self, *subs):
        current = self.get_tutor_subjects()
        for x in subs:
            if x not in current:
                current.append(x)
        self.set_tutor_subjects(current)
    def remove_tutor_subject(self, *subs):
        current = self.get_tutor_subjects()
        for x in subs:
            try:
                current.remove(x)
            except ValueError:
                pass
        self.set_tutor_subjects(current)
