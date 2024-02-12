from django.urls import path
from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("login/", views.login, name="login"),
	path("login/<int:new_user>/", views.login, name="login_new_user"),
	path("logout/", views.logout, name="logout"),
	path("create_account/", views.create_account, name="create_account"),
	path("verify_account/<str:email_key>/", views.verify_account, name="verify_account"),
	path("profile/<str:username>/", views.profile, name="profile"),
]
