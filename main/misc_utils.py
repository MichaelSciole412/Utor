from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from .forms import *
from .models import *
import string
import random
import requests

def ensure_authenticated(target):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        return target(request, *args, **kwargs)
    return wrapper

def ensure_not_authenticated(target):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("index")
        return target(request, *args, **kwargs)
    return wrapper

def generate_email_key():
    rand_chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    key = "".join(random.choice(rand_chars) for _ in range(50))
    return key

def domain_util(full_domain, remove_n=0):
    return ".".join(full_domain.split(".")[remove_n:])

def is_url_image(image_url):
    try:
        r = requests.head(image_url)
        if r.headers["content-type"].startswith("image"):
            return True
    except:
        pass
    return False

def user_tag_util(group_id, request_username, post_id):
    def check_and_notify(s_match):
        username = s_match.group()[1:]
        user_exists = User.objects.filter(username=username).exists()
        group = StudyGroup.objects.get(pk=group_id)
        if user_exists:
            u = User.objects.get(username=username)
            if group.user_list.contains(u):
                note = Notification()
                note.user = u
                note.n_type = "post"
                note.title = f"{request_username} tagged you in a post"
                note.text = f"{request_username} tagged you in a post in {group.name}.  Click the link below to see the post."
                note.regarding_post = GroupPost.objects.get(pk=post_id)
                note.save()
            return "<a class='userlink' href='" + reverse("profile", kwargs={"username": username}) + "'>" + s_match.group() + "</a>"
        else:
            return s_match.group()
    return check_and_notify
