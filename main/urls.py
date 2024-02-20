from django.urls import include, path
from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("login/", views.login, name="login"),
	path("login/<int:new_user>/", views.login, name="login_new_user"),
	path("logout/", views.logout, name="logout"),
	path("create_account/", views.create_account, name="create_account"),
	path("verify_account/<str:email_key>/", views.verify_account, name="verify_account"),
	path("profile/<int:user_id>/", views.profile_by_id, name="profile_by_id"),
	path("profile/<str:username>/", views.profile, name="profile"),
	path('tutor_search/', views.tutor_search, name='tutor_search'),
	path('enable_tutoring/<str:username>/', views.enable_tutoring, name='enable_tutoring'),
	path("groups/", views.study_groups, name="study_groups"),
	path("groups/create_study_group/", views.create_study_group, name="create_study_group"),
	path("groups/view_group/<int:group_id>/", views.view_group, name="view_group"),
	path("notifications/", views.notifications, name="notifications"),
	path("ajax/save_desc/<int:group_id>/", views.save_desc, name="save_desc"),
	path("ajax/save_bio/<str:username>/", views.save_bio, name="save_bio"),
	path("ajax/save_zip/<str:username>/", views.save_zip, name="save_zip"),
	path("ajax/save_pay/<str:username>/", views.save_pay, name="save_pay"),
 	path("ajax/add_subject/<str:username>/", views.add_subject, name="add_subject"),
	path("ajax/remove_subject/<str:username>/", views.remove_subject, name="remove_subject"),
	path("ajax/add_tutoring/<str:username>/", views.add_tutoring, name="add_tutoring"),
	path("ajax/remove_tutoring/<str:username>/", views.remove_tutoring, name="remove_tutoring"),
	path("ajax/delete_notification/<int:notification_id>/", views.delete_notification, name="delete_notification"),
	path("ajax/request_join/<int:group_id>/", views.request_join, name="request_join"),
	path("ajax/accept_request/<int:group_id>/<int:user_id>/", views.accept_request, name="accept_request"),
	path("ajax/reject_request/<int:group_id>/<int:user_id>/", views.reject_request, name="reject_request"),
	path("ajax/leave_group/<int:group_id>/", views.leave_group, name="leave_group"),
]

