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

    @staticmethod
    def get_valid_domains():
        with open("main/static/main/valid_domains.txt") as vd:
            ret = eval(vd.read())
        return ret

class User(AbstractUser):
    tutor_subjects = models.TextField(null=True)
    student_subjects = models.TextField(null=True)
    university = models.ForeignKey(University, on_delete=models.PROTECT, null=True, blank=True)
    bio = models.TextField(default="This user hasn't set their bio")
    is_verified = models.BooleanField(default=False)
    email_key = models.CharField(max_length=50, unique=True)
    tutoring_enabled = models.BooleanField(default=False)
    tutoring_pay = models.DecimalField(null=True, decimal_places=2, max_digits=4, default=0.00)
    zip_code = models.IntegerField(null=True, default=28607)

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

    def get_student_subjects(self):
        return json.loads(self.student_subjects or "[]")
    def set_student_subjects(self, subjects):
        self.student_subjects = json.dumps(subjects)
        self.save()
    def add_student_subject(self, *subs):
        current = self.get_student_subjects()
        for x in subs:
            if x not in current:
                current.append(x)
        self.set_student_subjects(current)
    def remove_student_subject(self, *subs):
        current = self.get_student_subjects()
        for x in subs:
            try:
                current.remove(x)
            except ValueError:
                pass
        self.set_student_subjects(current)

    def has_notifications(self):
        return bool(Notification.objects.filter(user=self))

    def num_notifications(self):
        return len(Notification.objects.filter(user=self))

class StudyGroup(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_studygroups")
    university = models.ForeignKey(University, on_delete=models.CASCADE)
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
    def get_ordered_comments(self):
        return self.comment_set.order_by("time")


class Recipient_Group(models.Model):
    name = models.CharField(max_length=100, default="")
    users = models.ManyToManyField(User, related_name="recipient")

    def __str__(self):
        return self.name


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(GroupPost, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

class Conversation(models.Model):
    conversation_type = models.CharField(max_length=2, choices={"TM": "Tutor Message", "DM": "Direct Message", "GM": "Group Message"})
    users = models.ManyToManyField(User)

class Message(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent")
    recipents = models.ForeignKey(Recipient_Group, on_delete=models.CASCADE, related_name="recipient")

    def __str__(self):
        return f'{self.time} - {self.creator.username}'


class Notification(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    n_type = models.CharField(max_length=10)
    title = models.CharField(max_length = 150)
    text = models.CharField(max_length = 500)
    regarding_group = models.ForeignKey(StudyGroup, null=True, on_delete=models.CASCADE, related_name="gnot_set")
    regarding_user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="regu_set")
    regarding_post = models.ForeignKey(GroupPost, null=True, on_delete=models.CASCADE, related_name="regp_set")

class CurrentGroupChatUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)

    @staticmethod
    def create(user, group):
        q = CurrentGroupChatUser.objects.filter(user=user, group=group)
        if q.exists():
            return
        newcgu = CurrentGroupChatUser()
        newcgu.user = user
        newcgu.group = group
        newcgu.save()

class GroupChat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
