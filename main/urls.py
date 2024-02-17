from django.urls import include, path
from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("login/", views.login, name="login"),
	path("login/<int:new_user>/", views.login, name="login_new_user"),
	path("logout/", views.logout, name="logout"),
	path("create_account/", views.create_account, name="create_account"),
	path("verify_account/<str:email_key>/", views.verify_account, name="verify_account"),
	path("profile/<str:username>/", views.profile, name="profile"),
	path('tutor_search/', views.tutor_search, name='tutor_search'),
	path('enable_tutoring/<str:username>/', views.enable_tutoring, name='enable_tutoring'),
	path("groups/", views.study_groups, name="study_groups"),
	path("groups/create_study_group/", views.create_study_group, name="create_study_group"),
	path("groups/view_group/<int:group_id>/", views.view_group, name="view_group"),
	path("ajax/save_desc/<int:group_id>/", views.save_desc, name="save_desc"),
]

