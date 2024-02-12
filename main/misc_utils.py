from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from .forms import *
from .models import *
import string
import random

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
