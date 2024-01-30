from django.db import models
from django.contrib.auth.models import AbstractUser
import json
import datetime

class University(models.Model):
    name = models.CharField(max_length=150)
    domains = models.TextField(null=True)
    web_pages = models.TextField(null=True)
    country = models.CharField(max_length=50)
    alpha_two_code = models.CharField(max_length=10, null=True)
    state_province = models.CharField(max_length=100,null=True)

    def get_domains(self):
        return json.loads(self.domains or "[]")

    def get_webpages(self):
        return json.loads(self.web_pages or "[]")

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

class StudyGroup(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_studygroups")
    user_list = models.ManyToManyField(User)
    requests = models.ManyToManyField(User, related_name="requests_set")
    invitations = models.ManyToManyField(User, related_name="invitations_set")
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    course = models.CharField(max_length=10, null=True, blank=True)

class Meeting(models.Model):
    title = models.CharField(max_length=50)
    meet_time = models.DateTimeField(auto_now_add=False, auto_now=False)
    description = models.TextField(null=True, blank=True)
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)

    def has_passed(self):
        return self.meet_time < datetime.datetime.now()


class GroupPost(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length = 130)
    text = models.TextField(null=True, blank=True)
    image_source = models.CharField(max_length=1000, null=True, blank=True)

class Conversation(models.Model):
    conversation_type = models.CharField(max_length=2, choices={"TM": "Tutor Message", "DM": "Direct Message", "GM": "Group Message"})
    users = models.ManyToManyField(User)

class Message(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
