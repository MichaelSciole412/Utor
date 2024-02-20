from django import forms
from django.core.validators import EmailValidator, RegexValidator, ValidationError, MinLengthValidator
import re
from .models import *

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=50)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        if not User.objects.filter(username__iexact=username).exists():
            raise ValidationError(f"User {username} does not exist.")
        return username


class AccountForm(forms.Form):
    firstname = forms.CharField(label="First Name", max_length=50, validators=[RegexValidator(regex="^[a-zA-Z \-]+$", message="Enter a valid first name")])
    lastname = forms.CharField(label="Last Name", max_length=50, validators=[RegexValidator(regex="^[a-zA-Z \-]+$", message="Enter a valid last name")])
    username = forms.CharField(label="Username", max_length=50)
    email = forms.EmailField(label="Email", max_length=100)
    password = forms.CharField(label="Password", validators=[RegexValidator(regex="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", message="Password must be at least 8 characters and contain at least 1 letter and one number")], widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm Password", validators=[], widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("User with this email address already exists")
        valid_domains = University.get_valid_domains()
        for domain in valid_domains:
            if email.endswith(domain):
                return email
        raise ValidationError("The email address you provide must be associated with a university")

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("Username already in use")
        if not username or not re.match("^[a-zA-Z0-9\-_]+$", username):
            raise ValidationError("Username must contain only letters, numbers, underscores, and dashes")
        if not re.match("^.*[a-zA-Z].*$", username):
            raise ValidationError("Username must contain at least one letter")
        if len(username) > 50:
            raise ValidationError("Username must be less than or equal to 50 characters")
        return username

    def clean(self):
        cleaned_data = super(AccountForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError("Passwords don't match")
        return cleaned_data

class StudyGroupForm(forms.Form):
    group_name = forms.CharField(label="Study Group Name", max_length=50, validators=[RegexValidator(regex="^\S.{4,}$", message="Group name must be at least 5 characters")])
    subject = forms.CharField(label="Subject", max_length=50, validators=[RegexValidator(regex="^\S.*$", message="Subject must not be blank")])
    course = forms.CharField(label="Course Prefix and Number (optional)", required=False, validators=[RegexValidator(regex="^[A-Za-z_]{2,3} \d{1,5}$", message="Invalid course prefix and number")])
    description = forms.CharField(label="Description", widget=forms.Textarea(attrs={"rows": "5"}))
