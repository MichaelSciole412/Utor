from django.urls import path
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
	path("groups/", views.study_groups, name="study_groups"),
	path("groups/create_study_group/", views.create_study_group, name="create_study_group"),
	path("groups/view_group/<int:group_id>/", views.view_group, name="view_group"),
	path("notifications/", views.notifications, name="notifications"),
	path("ajax/save_desc/<int:group_id>/", views.save_desc, name="save_desc"),
	path("ajax/delete_notification/<int:notification_id>/", views.delete_notification, name="delete_notification"),
	path("ajax/request_join/<int:group_id>/", views.request_join, name="request_join"),
	path("ajax/accept_request/<int:group_id>/<int:user_id>/", views.accept_request, name="accept_request"),
	path("ajax/reject_request/<int:group_id>/<int:user_id>/", views.reject_request, name="reject_request"),
	path("ajax/leave_group/<int:group_id>/", views.leave_group, name="leave_group"),
]
