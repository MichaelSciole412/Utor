from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login as log_in, logout as log_out
from .misc_utils import *
from django.core.mail import send_mail
import time

@ensure_authenticated
def index(request):
    return render(request, "index.html", context=None)

@ensure_authenticated
def logout(request):
    log_out(request)
    return redirect(reverse("login"))


@ensure_not_authenticated
def login(request, new_user=0):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            usr = User.objects.get(username__iexact=form.cleaned_data['username'])
            if not authenticate(username=usr.username, password=form.cleaned_data['password']):
                return render(request, "login.html", {'form': form, 'message': "Invalid login information."})
            elif not usr.is_verified:
                return render(request, "login.html", {'form': form, 'message': "Please Verify Your Email Before Logging in."})
            else:
                log_in(request, authenticate(username=usr.username, password=form.cleaned_data['password']))
                return HttpResponseRedirect(reverse("index"))
    message = None
    if new_user == 1:
        message = "Account Created. Check Email to Verify Account."
    return render(request, "login.html", context={"form": form, "message": message})

@ensure_not_authenticated
def create_account(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            new_user = User()
            new_user.username = form.cleaned_data['username']
            new_user.set_password(form.cleaned_data['password'])
            new_user.first_name = form.cleaned_data['firstname']
            new_user.last_name = form.cleaned_data['lastname']
            new_user.email = form.cleaned_data['email'].lower()
            new_user.email_key = generate_email_key()
            send_mail(
                "Verify You Utor Account",
                "Click the Link: " + request.build_absolute_uri(f"/verify_account/{new_user.email_key}/"),
                "utor.service@gmail.com",
                [new_user.email],
                fail_silently=False,
            )
            # Find which university their email address is associated with
            # Yes, this doesn't look elegant, but its the best way I promise
            email_domain = new_user.email.split("@")[1]
            for n in range(len(email_domain.split("."))):
                if University.objects.filter(domains__contains=domain_util(email_domain, n)).exists():
                    uni = University.objects.filter(domains__contains=domain_util(email_domain, n))[0]
                    new_user.university = uni
                    break

            new_user.save()
            return redirect(reverse("login_new_user", kwargs={"new_user": 1}))
        return render(request, "create_account.html", context={"form": form})
    form = AccountForm()
    return render(request, "create_account.html", context={"form": form})

def verify_account(request, email_key=""):
    if not User.objects.filter(email_key=email_key).exists():
        return redirect(reverse("login"))
    else:
        usr = User.objects.get(email_key=email_key)
        usr.is_verified = True
        usr.save()
        return render(request, "verify_account.html", context={"username": usr.username})

@ensure_authenticated
def profile(request, username=""):
    usr = get_object_or_404(User, username=username)
    current_user = usr.username == request.user.username
    if request.method == "POST" and current_user:
        if request.POST.get("new_subject") is not None:
            usr.add_student_subject(request.POST.get("new_subject"))
            return redirect(reverse("profile", kwargs={"username": username}))
        if request.POST.get("remove_subject") is not None:
            usr.remove_student_subject(request.POST.get("remove_subject"))
            return redirect(reverse("profile", kwargs={"username": username}))
    return render(request, "profile.html", context={"user": usr, "current_user": current_user})
