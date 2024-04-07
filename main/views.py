from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, Http404, HttpResponseServerError, JsonResponse, HttpRequest, StreamingHttpResponse
from django.utils.html import escape, format_html, smart_urlquote
from django.template import loader
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.utils.dateformat import DateFormat
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login as log_in, logout as log_out
from .misc_utils import *
from django.core.mail import send_mail
import time
import re

# Imports for messaging
import asyncio
from typing import AsyncGenerator
from . import models
import random

def create_message_group(request, username):
    user = get_object_or_404(User, username=request.user.username)

    tutors = User.objects.filter(username=username)
    tutor = tutors.first()

    existing_group = Recipient_Group.objects.filter(users=user).filter(users=tutor).first()
    if existing_group:
        return redirect(reverse("message_page"))

    recipient_group = Recipient_Group.objects.create()
    recipient_group.users.add(user, tutor)
    recipient_group.save()
    return redirect(reverse("message_page"))

def message_page(request):
    user = get_object_or_404(User, username=request.user.username)
    user_groups = Recipient_Group.objects.filter(users=user).all()

    return render(request, 'messages.html', {'user_groups': user_groups})

def send_message(request, group_id):
    user = user = get_object_or_404(User, username=request.user.username)
    group = get_object_or_404(Recipient_Group, id=group_id, users=user)

    message = request.POST.get('message', '')

    if message:
        msg = Message.objects.create(
            text=message,
            creator=user,
        )
        msg.recipents.add(group.id)

    return render(request, 'send_message.html', {'group_id': group_id})






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
def profile_by_id(request, user_id):
    usr = get_object_or_404(User, pk=user_id)
    return redirect(reverse("profile", kwargs={"username": usr.username}))

@ensure_authenticated
def profile(request, username):
    usr = get_object_or_404(User, username=username)
    current_user = usr.username == request.user.username
    '''if request.method == "POST" and current_user:
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
            return redirect(reverse("profile", kwargs={"username": username}))'''
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

ZIP_WISE_KEY = 'atue9sehje6s9kav'
ZIP_WISE_API_ENDPOINT = 'https://www.zipwise.com/webservices/'
import requests
from django.db.models import Case, When, Value, IntegerField

@ensure_authenticated
def tutor_search(request):
	query = request.GET.get('subject', '')
	filter_type = request.GET.get('filter-type', 'no-filter')
	filter_query = request.GET.get('filter-query', '')
	tutors = User.objects.filter(tutor_subjects__icontains=query, tutoring_enabled = True).exclude(username=request.user);

	zip_url = '{}radius.php?key={}&zip={}&radius=5&format=json'.format(ZIP_WISE_API_ENDPOINT, ZIP_WISE_KEY, filter_query)
	if filter_type == 'username' and filter_query:
		partials = tutors.filter(username__icontains=filter_query)
		tutors = tutors.filter(username__iexact=filter_query).union(partials).order_by('username')
	elif filter_type == 'zip-code':
		try:
			response = requests.get(zip_url)
			response.raise_for_status()
		except requests.RequestException as e:
			return HttpResponseServerError("Internal Server Error")

		if response.status_code == 200:
			zip_data = response.json()
			prox_data = zip_data.get('results', [])
			zip_codes = [result['zip'] for result in prox_data]
			exact_zip = [zip_code for zip_code in zip_codes if zip_code == filter_query]
			inexact_zip = [zip_code for zip_code in zip_codes if zip_code != filter_query]
			ordered_prox = exact_zip + inexact_zip

			ordering = Case(
    			*[When(zip_code=zip_code, then=Value(i, output_field=IntegerField())) for i, zip_code in enumerate(ordered_prox)]
			)

			tutors = tutors.filter(zip_code__in=ordered_prox).order_by(ordering)

	return render(request, 'tutor_search.html', {'tutors': tutors, 'query': query, 'filter_type': filter_type, 'filter_query': filter_query})

@csrf_exempt
@ensure_authenticated
def study_groups(request):
    my_groups = StudyGroup.objects.filter(user_list=request.user)
    base = StudyGroup.objects.filter(university=request.user.university)
    rec_groups = StudyGroup.objects.none()
    search = False
    if 'search' in request.GET and request.GET.get('search', ''):
        search = True
        query = request.GET.get("search", "")
        if re.match("^[A-Za-z_]{2,3} \d{1,5}$", query):
            rec_groups |= base.filter(course__iexact=query).exclude(user_list=request.user)
        if User.objects.filter(username__iexact=query).exists():
            rec_groups |= base.filter(owner__username__iexact=query).exclude(user_list=request.user)
        if base.filter(subject__iexact=query).exists():
            rec_groups |= base.filter(subject__iexact=query).exclude(user_list=request.user)
        rec_groups |= base.filter(name__iexact=query).exclude(user_list=request.user)
        rec_groups |= base.filter(name__icontains=query).exclude(user_list=request.user)
        rec_groups |= base.filter(subject__icontains=query).exclude(user_list=request.user)
        rec_groups |= base.filter(owner__username__icontains=query).exclude(user_list=request.user)
    else:
        for subject in request.user.get_student_subjects():
            rec_groups |= base.filter(subject__iexact=subject).exclude(user_list=request.user)
        for subject in request.user.get_student_subjects():
            rec_groups |= base.filter(name__iexact=subject).exclude(user_list=request.user)

        for subject in request.user.get_student_subjects():
            rec_groups |= base.filter(subject__icontains=subject).exclude(user_list=request.user)
        for subject in request.user.get_student_subjects():
            rec_groups |= base.filter(name__icontains=subject).exclude(user_list=request.user)


    p = Paginator(rec_groups, 10)
    if 'page' in request.GET:
        page_num = request.GET.get('page')
        try:
            page_num = int(page_num)
        except:
            pass
        if page_num not in p.page_range: raise Http404(f"Page {request.GET.get('page')} does not exist")
        page = p.page(request.GET['page'])
        for x in page:
            print(x.name)
    else:
        page = p.page(1)

    context = {"my_groups": my_groups, "rec_groups": page, "search": search, "p": p}
    if 'search' in request.GET and request.GET.get('search', ''): context["query"] = request.GET.get('search', '')

    return render(request, "study_groups.html", context=context)

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
    posts = group.grouppost_set.order_by("-time")
    usr_in_group = group.user_list.contains(request.user)
    meetings = Meeting.objects.filter(group=group).filter(time__gt = timezone.now()).order_by("time")
    next_meeting = False
    if meetings.exists():
        next_meeting = meetings[0]
    return render(request, "view_group.html", context={"group": group, "usr_in_group": usr_in_group, "posts": posts, "next_meeting": next_meeting})

@ensure_authenticated
def notifications(request):
    notifs = Notification.objects.filter(user=request.user).order_by("-time")
    return render(request, "notifications.html", context={"notifications": notifs})

@ensure_authenticated
def make_post(request, group_id):
    group = get_object_or_404(StudyGroup, pk=group_id)
    if not group.user_list.contains(request.user):
        return redirect(reverse("view_group", kwargs={"group_id": group_id}))
    form = GroupPostForm()
    if request.method == "POST":
        form = GroupPostForm(request.POST)
        if form.is_valid():
            new_post = GroupPost()
            new_post.poster = request.user
            new_post.group = group
            new_post.title = form.cleaned_data["title"]
            if form.cleaned_data["image_source"]:
                new_post.image_source = form.cleaned_data["image_source"]
            new_post.save()
            if form.cleaned_data["text"]:
                temp = escape(form.cleaned_data["text"])
                temp = re.sub("(&[a-z]+;|&#\d+;)", "\n\g<0>\n", temp)
                temp = re.sub("\[(.+)\]\(((https://|http://|www\.)\S*)\)", "<a class='postlink' href=\"\g<2>\">\g<1></a>", temp)
                temp = re.sub("((?<!href=\")(?<!href=\"http://)(?<!href=\"https://)(https://|http://|www\.)\S*)", "<a class='postlink' href=\"\g<0>\">\g<0></a>", temp)
                temp = re.sub("\n(&[a-z]+;|&#\d+;)\n", "\g<1>", temp)
                temp = re.sub("@[a-zA-Z0-9\-_]{1,50}", user_tag_util(group.id, request.user.username, new_post.id), temp)
                new_post.text = temp
            new_post.save()



            return redirect(reverse("view_group", kwargs={"group_id": group_id}))

    return render(request, "make_post.html", context={"form": form, "group": group})

@ensure_authenticated
def join_group(request, group_id):
    group = get_object_or_404(StudyGroup, pk=group_id)
    if group.invitations.contains(request.user):
        group.invitations.remove(request.user)
        group.requests.remove(request.user)
        group.user_list.add(request.user)

        note = Notification()
        note.user = group.owner
        note.n_type = "group"
        note.title = f"{request.user.username} has joined {group.name}"
        note.text = f"{request.user.username} has accepted your invitation to join {group.name}"
        note.regarding_group = group
        note.save()

    return redirect(reverse("view_group", kwargs={"group_id": group_id}))

@ensure_authenticated
def group_chat(request, group_id):
    group = get_object_or_404(StudyGroup, pk=group_id)
    if group.user_list.contains(request.user):
        return render(request, "group_chat.html", context={"group": group})
    return redirect(reverse("view_group", kwargs={"group_id": group_id}))

@ensure_authenticated
def schedule(request, group_id, past=False):
    group = get_object_or_404(StudyGroup, pk=group_id)
    if group.user_list.contains(request.user):
        if not past:
            meeting_list = Meeting.objects.filter(group=group).filter(time__gt = timezone.now()).order_by("time")
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            return render(request, "schedule.html", context={"group": group, "meeting_list": meeting_list, "current_date": current_date, "past": False})
        elif past == "past":
            meeting_list = Meeting.objects.filter(group=group).filter(time__lt = timezone.now()).order_by("-time")
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            return render(request, "schedule.html", context={"group": group, "meeting_list": meeting_list, "current_date": current_date, "past": True})
        else:
            raise Http404()
    return redirect(reverse("view_group", kwargs={"group_id": group_id}))

### AJAX

@csrf_exempt
@ensure_authenticated
def save_desc(request, group_id):
    request_data = json.loads(request.body)
    group = get_object_or_404(StudyGroup, pk=group_id)
    if request.user == group.owner:
        group.description = request_data['desc'][:500]
        group.save()
        return HttpResponse("CONFIRM")
    return HttpResponse("DENY")

@csrf_exempt
@ensure_authenticated
def save_bio(request, username=""):
    request_data = json.loads(request.body)
    usr = get_object_or_404(User, username=username)
    if usr.username == request.user.username:
        usr.bio = request_data['bio']
        usr.save()
        return HttpResponse("CONFIRM")


@csrf_exempt
@ensure_authenticated
def save_zip(request, username=""):
    if request.method == "POST":
        request_data = json.loads(request.body)
        zip_code = request_data.get("zip")
        zip_url = '{}zipinfo.php?key={}&zip={}&radius=5&format=json'.format(ZIP_WISE_API_ENDPOINT, ZIP_WISE_KEY, zip_code)
        try:
            response = requests.get(zip_url)
            response.raise_for_status()
        except requests.RequestException as e:
            return HttpResponseServerError("Internal Server Error")

        if response.status_code == 200:
            zip_data = response.json()
            print(zip_data)
            is_error = zip_data.get('results', [])
            if 'error' in is_error:
                msg = is_error['error]']
                return HttpResponseBadRequest("{msg}")
            else:
                usr = get_object_or_404(User, username=username)
                usr.zip_code = zip_code
                usr.save()
                return HttpResponse("ZIP code saved successfully")

    return HttpResponseBadRequest("invalid Zip Code")


@csrf_exempt
@ensure_authenticated
def save_pay(request, username=""):
    if request.method == "POST":
        request_data = json.loads(request.body)
        pay_rate = request_data.get("pay")

        if pay_rate is not None:
            usr = get_object_or_404(User, username=username)
            usr.tutoring_pay = pay_rate
            usr.save()
            return HttpResponse("Pay rate saved successfully")

    return HttpResponseBadRequest("invalid Pay Rate")


@csrf_exempt
@ensure_authenticated
def add_subject(request, username=""):
    if request.method == "POST":
        request_data = json.loads(request.body)
        usr = get_object_or_404(User, username=username)
        if usr.username == request.user.username:
            new_subject = request_data.get("new_subject")
            if new_subject:
                usr.add_student_subject(new_subject)
                return JsonResponse({"status": "CONFIRM"})
    return JsonResponse({"error": "Invalid Request"}, status=400)


@csrf_exempt
@ensure_authenticated
def remove_subject(request, username=""):
    if request.method == "POST":
        request_data = json.loads(request.body)
        usr = get_object_or_404(User, username=username)
        if usr.username == request.user.username:
            subject_to_rm = request_data.get("subject")
            if subject_to_rm:
                usr.remove_student_subject(subject_to_rm)
                return JsonResponse({"status": "CONFIRM"})
    return JsonResponse({"error": "Invalid Request"}, status=400)


@csrf_exempt
@ensure_authenticated
def add_tutoring(request, username=""):
    if request.method == "POST":
        request_data = json.loads(request.body)
        usr = get_object_or_404(User, username=username)
        if usr.username == request.user.username:
            new_tutoring = request_data.get("new_tutoring")
            if new_tutoring:
                usr.add_tutor_subject(new_tutoring)
                return JsonResponse({"status": "CONFIRM"})
    return JsonResponse({"error": "Invalid Request"}, status=400)


@csrf_exempt
@ensure_authenticated
def remove_tutoring(request, username=""):
    if request.method == "POST":
        request_data = json.loads(request.body)
        usr = get_object_or_404(User, username=username)
        if usr.username == request.user.username:
            tutoring_to_rm = request_data.get("tutoring")
            if tutoring_to_rm:
                usr.remove_tutor_subject(tutoring_to_rm)
                return JsonResponse({"status": "CONFIRM"})
    return JsonResponse({"error": "Invalid Request"}, status=400)

@csrf_exempt
@ensure_authenticated
def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, pk=notification_id)
    if request.user == notification.user:
        notification.delete()
        return HttpResponse("CONFIRM")
    return HttpResponse("DENY")

@csrf_exempt
@ensure_authenticated
def request_join(request, group_id):
    group = get_object_or_404(StudyGroup, pk=group_id)
    group.requests.add(request.user)
    group.save()

    note = Notification()
    note.user = group.owner
    note.n_type = "group"
    note.title = f"{request.user.username} has requested to join {group.name}"
    note.text = f"{request.user.username} wants to join {group.name}.  Accept or deny this request on {group.name}'s home page."
    note.regarding_group = group
    note.save()

    return HttpResponse("CONFIRM")

@csrf_exempt
@ensure_authenticated
def accept_request(request, group_id, user_id):
    group = get_object_or_404(StudyGroup, pk=group_id)
    new_usr = get_object_or_404(User, pk=user_id)
    if request.user == group.owner and group.requests.contains(new_usr):
        group.requests.remove(new_usr)
        group.invitations.remove(new_usr)
        group.user_list.add(new_usr)

        note = Notification()
        note.user = new_usr
        note.n_type = "group"
        note.title = f"You have joined {group.name}"
        note.text = f"{request.user} has accepted your request to join {group.name}!  Click below to go to the study group's homepage."
        note.regarding_group = group
        note.save()

        return HttpResponse("CONFIRM")
    return HttpResponse("DENY")

@csrf_exempt
@ensure_authenticated
def reject_request(request, group_id, user_id):
    group = get_object_or_404(StudyGroup, pk=group_id)
    new_usr = get_object_or_404(User, pk=user_id)
    if request.user == group.owner and group.requests.contains(new_usr):
        group.requests.remove(new_usr)
        return HttpResponse("CONFIRM")
    return HttpResponse("DENY")

@csrf_exempt
@ensure_authenticated
def leave_group(request, group_id):
    group = get_object_or_404(StudyGroup, pk=group_id)
    if group.user_list.contains(request.user):
        group.user_list.remove(request.user)
        return HttpResponse("CONFIRM")
    return HttpResponse("DENY")

@csrf_exempt
@ensure_authenticated
def kick_user(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        group = get_object_or_404(StudyGroup, pk=request_data["group_id"])
        usr = get_object_or_404(User, pk=request_data["user_id"])
        if request.user == group.owner and usr != group.owner:
            group.user_list.remove(usr)

            note = Notification()
            note.user = usr
            note.title = f"You have been kicked out of {group.name}"
            note.text = f"{request.user} has kicked you from {group.name}."
            note.regarding_group = group
            note.save()

            return JsonResponse({"status": "CONFIRM"})
    return JsonResponse({"error": "Invalid Request"}, status=400)

@csrf_exempt
@ensure_authenticated
def invite(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        group = get_object_or_404(StudyGroup, pk=request_data["group_id"])
        if request.user == group.owner:
            invite_username = request_data["username"]
            if User.objects.filter(username=invite_username).exists():
                invite_user = User.objects.get(username=invite_username)

                if group.invitations.contains(invite_user):
                    return HttpResponse("An invitation has already been sent")
                if group.user_list.contains(invite_user):
                    return HttpResponse("This user is already in the group")
                else:
                    group.invitations.add(invite_user)

                    note = Notification()
                    note.user = invite_user
                    note.n_type = "group"
                    note.title = f"You have been invited to join {group.name}"
                    note.text = f"{request.user} has invited you to join {group.name}!  You can accept this request on the study group homepage. Click the link below to go to the study group's homepage."
                    note.regarding_group = group
                    note.save()

                    return HttpResponse("Invite Sent!")
            else:
                return HttpResponse(f"User {invite_username} does not exist")

    return HttpResponse("DENY")

@csrf_exempt
@ensure_authenticated
def make_comment(request):
    request_data = json.loads(request.body)
    group = get_object_or_404(StudyGroup, pk=request_data["group_id"])
    post = get_object_or_404(GroupPost, pk=request_data["post_id"])
    comment_text = request_data["comment"]
    if group.user_list.contains(request.user):
        comment = Comment()
        comment.author = request.user
        comment.post = post
        temp = escape(comment_text)
        temp = re.sub("(&[a-z]+;|&#\d+;)", "\n\g<0>\n", temp)
        temp = re.sub("\[(.+)\]\(((https://|http://|www\.)\S*)\)", "<a class='postlink' href=\"\g<2>\">\g<1></a>", temp)
        temp = re.sub("((?<!href=\")(?<!href=\"http://)(?<!href=\"https://)(https://|http://|www\.)\S*)", "<a class='postlink' href=\"\g<0>\">\g<0></a>", temp)
        temp = re.sub("\n(&[a-z]+;|&#\d+;)\n", "\g<1>", temp)
        temp = re.sub("@[a-zA-Z0-9\-_]{1,50}", user_tag_util(group.id, request.user.username, post.id), temp)
        comment.text = temp
        comment.save()

        date_formatter = DateFormat(comment.time)
        time_str = date_formatter.format("n/j/y g:i") + "&nbsp;" + date_formatter.format("A")
        break_fix_ct = comment.text.replace('\n', '<br/>')
        response_html = f"""
                        <div class="comment">
                            <div class="flexrow center">
                              <div style="width: 80%;"><h5 style="margin-top: 5px; margin-bottom: 15px;"><a class="userlink" href="/profile/{comment.author.username}/">{ comment.author.username }</a></h5></div>
                              <div style="text-align: right; font-size: 11px; color: gray; width: 20%;">{time_str}</div>
                            </div>
                            { break_fix_ct }
                        </div>"""

        return HttpResponse(response_html)

    return HttpResponse("DENY")

@csrf_exempt
@ensure_authenticated
def make_schedule_item(request):
    request_data = json.loads(request.body)
    group = get_object_or_404(StudyGroup, pk=request_data["group_id"])
    if group.owner == request.user:
        time = request_data['time']
        date = request_data['date']

        dt = datetime.datetime.strptime(date+" "+time, '%Y-%m-%d %H:%M')
        dt_aware = timezone.make_aware(dt)

        m = Meeting()
        m.group = group
        m.title = request_data['title']
        m.time = dt_aware
        m.duration_hours = request_data['duration_hours']
        m.duration_minutes = request_data['duration_minutes']
        m.location = request_data['location']
        m.description = request_data['description']
        m.save()

        for usr in group.user_list.all():
            if usr != group.owner:
                note = Notification()
                note.user = usr
                note.n_type = "group"
                note.title = f"A New Meeting Has Been Scheduled for {group.name}"
                note.text = f"A new meeting has been scheduled on {dt_aware.strftime('%-m/%-d/%y')} for {group.name}. Click the link below to go to the study group's homepage."
                note.regarding_group = group
                note.save()

        return HttpResponse(str(m.id))

    return HttpResponse("DENY");


@csrf_exempt
@ensure_authenticated
def remove_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    group = meeting.group
    if request.user == group.owner:
        for usr in group.user_list.all():
            if usr != group.owner:
                note = Notification()
                note.user = usr
                note.n_type = "group"
                note.title = f"A Meeting Has Been Removed From the Schedule For {group.name}"
                note.text = f"{meeting.title} on {meeting.time.strftime('%-m/%-d/%y')} has been removed from the meeting schedule of {group.name}."
                note.regarding_group = group
                note.save()
        meeting.delete()
        return HttpResponse("CONFIRM")
    return HttpResponse("DENY")

@csrf_exempt
@ensure_authenticated
def delete_group(request):
    request_data = json.loads(request.body)
    group = get_object_or_404(StudyGroup, pk=request_data["group_id"])
    if request.user == group.owner:
        for usr in group.user_list.all():
            if usr != group.owner:
                note = Notification()
                note.user = usr
                note.title = f"A Study Group You Are in Has Been Deleted"
                note.text = f"User {request.user} has deleted {group.name}.  This study group will no longer appear in your groups list."
                note.save()
        group.delete()
        return HttpResponse("CONFIRM")
    return HttpResponse("DENY")
