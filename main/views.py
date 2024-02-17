from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
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
        if request.POST.get("new_tutor_subject") is not None:
            usr.add_tutor_subject(request.POST.get("new_tutor_subject"))
            return redirect(reverse("profile", kwargs={"username": username}))
        if request.POST.get("remove_tutor_subject") is not None:
            usr.remove_tutor_subject(request.POST.get("remove_tutor_subject"))
            return redirect(reverse("profile", kwargs={"username": username}))
        if request.POST.get("tutoring_rate") is not None:
            usr.tutoring_pay = request.POST.get("tutoring_rate")
            usr.save()
            return redirect(reverse("profile", kwargs={"username": username}))
        if request.POST.get("zip_code") is not None:
            usr.zip_code = request.POST.get("zip_code")
            usr.save()
            return redirect(reverse("profile", kwargs={"username": username}))
        if request.POST.get("bio") is not None:
            usr.bio = request.POST.get("bio")
            usr.save()
            return redirect(reverse("profile", kwargs={"username": username}))
    return render(request, "profile.html", context={"user": usr, "current_user": current_user})

@ensure_authenticated
def enable_tutoring(request, username=""):
    usr = get_object_or_404(User, username=username)
    
    if request.method == "POST" and usr.username == request.user.username:
        if usr.tutoring_enabled == False:
            usr.tutoring_enabled = True
            usr.save()
        else:
            usr.tutoring_enabled = False
            usr.save()
    return redirect(reverse("profile", kwargs={"username": username}))

@ensure_authenticated
def tutor_search(request):
	query = request.GET.get('subject', '')
 
	filter_type = request.GET.get('filter-type', 'no-filter')
	filter_query = request.GET.get('filter-query', '')
	
	tutors = User.objects.filter(tutor_subjects__icontains=query, tutoring_enabled = True)

	if filter_type == 'username' and filter_query:
		partials = tutors.filter(username__icontains=filter_query)
		tutors = tutors.filter(username__iexact=filter_query).union(partials).order_by('username')
	elif filter_type == 'zip-code':
		tutors = tutors.filter(tutor_zipcode__icontains=filter_query)
	
	
	return render(request, 'tutor_search.html', {'tutors': tutors, 'query': query, 'filter_type': filter_type, 'filter_query': filter_query})

def study_groups(request):
    my_groups = StudyGroup.objects.filter(user_list=request.user)
    base = StudyGroup.objects.filter(university=request.user.university)
    rec_groups = StudyGroup.objects.none()
    for subject in request.user.get_student_subjects():
        rec_groups |= base.filter(subject__iexact=subject).exclude(user_list=request.user)
    for subject in request.user.get_student_subjects():
        rec_groups |= base.filter(subject__icontains=subject).exclude(user_list=request.user)


    return render(request, "study_groups.html", context={"my_groups": my_groups, "rec_groups": rec_groups})

@ensure_authenticated
def create_study_group(request):
    form = StudyGroupForm()
    if request.method == "POST":
        form = StudyGroupForm(request.POST)
        if form.is_valid():
            new_group = StudyGroup()
            new_group.owner = request.user
            new_group.university = request.user.university
            new_group.name = form.cleaned_data["group_name"]
            new_group.subject = form.cleaned_data["subject"]
            if form.cleaned_data["course"]:
                new_group.course = form.cleaned_data["course"]
            new_group.description = form.cleaned_data["description"]
            new_group.save()
            new_group.user_list.add(request.user)
            return redirect(reverse("study_groups"))
    return render(request, "create_study_group.html", context={"form": form})

@ensure_authenticated
def view_group(request, group_id):
    group = get_object_or_404(StudyGroup, pk=group_id)
    usr_in_group = request.user in group.user_list.all()
    return render(request, "view_group.html", context={"group": group, "usr_in_group": usr_in_group})

### AJAX

@csrf_exempt
@ensure_authenticated
def save_desc(request, group_id):
    request_data = json.loads(request.body)
    group = get_object_or_404(StudyGroup, pk=group_id)
    if request.user == group.owner:
        group.description = request_data['desc']
        group.save()
        return HttpResponse("CONFIRM")
