from django.urls import include, path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve


urlpatterns = [
	path("", views.index, name="index"),
	path("login/", views.login, name="login"),
	path("login/<int:new_user>/", views.login, name="login_new_user"),
	path("logout/", views.logout, name="logout"),
	path("create_account/", views.create_account, name="create_account"),
	path("verify_account/<str:email_key>/", views.verify_account, name="verify_account"),
	path("profile/<int:user_id>/", views.profile_by_id, name="profile_by_id"),
	path("profile/<str:username>/", views.profile, name="profile"),
	path("tutor_profile/<str:tutor>/", views.tutor_profile, name='tutor_profile'),
	path('tutor_search/', views.tutor_search, name='tutor_search'),
	path('create_message_group/<str:username>', views.create_message_group, name='create_message_group'),
    path('review_page/<str:tutor>', views.review_page, name="review_page"),
    path('reviews/<str:username>', views.user_reviews, name='user_reviews'),
	path('message_page/', views.message_page, name='message_page'),
	path('send_message/<str:dmid>/', views.send_message, name='send_message'),
	path('enable_tutoring/<str:username>/', views.enable_tutoring, name='enable_tutoring'),
	path("groups/", views.study_groups, name="study_groups"),
	path("groups/create_study_group/", views.create_study_group, name="create_study_group"),
	path("groups/view_group/<int:group_id>/", views.view_group, name="view_group"),
	path("groups/view_group/<int:group_id>/make_post/", views.make_post, name="make_post"),
	path("groups/view_group/<int:group_id>/group_chat/", views.group_chat, name="group_chat"),
	path("groups/view_group/<int:group_id>/schedule/", views.schedule, name="schedule"),
	path("groups/view_group/<int:group_id>/schedule/<str:past>/", views.schedule, name="schedule_past"),
	path("notifications/", views.notifications, name="notifications"),
	path("join_group/<int:group_id>/", views.join_group, name="join_group"),
	path('ajax/setOverall/<str:tutor>', views.setOverall, name="setOverall"),
	path('ajax/setEffective/<str:tutor>', views.setEffective, name="setEffective"),
	path('ajax/setTime/<str:tutor>', views.setTime, name="setTime"),
 	path('ajax/setPatience/<str:tutor>', views.setPatience, name="setPatience"),
	path('ajax/setKnowledge/<str:tutor>', views.setKnowledge, name="setKnowledge"),
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
	path("ajax/kick_user/", views.kick_user, name="kick_user"),
	path("ajax/invite/", views.invite, name="invite"),
	path("ajax/make_comment/", views.make_comment, name="make_comment"),
	path("ajax/schedule/", views.make_schedule_item, name="make_schedule_item"),
	path("ajax/remove_meeting/<int:meeting_id>/", views.remove_meeting, name="remove_meeting"),
	path("ajax/delete_group/", views.delete_group, name="delete_group"),
	re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
