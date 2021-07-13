from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("details/<int:pk>/", views.MeetingDetailView.as_view(), name="meeting_details"),
    path("checkin/<uuid:slug>", views.checkin_view, name="meeting_checkin"),
    path("update/<int:pk>/", views.update_meeting, name="update_meeting"),
    path("delete/<int:pk>/", views.delete_meeting, name="delete_meeting"),
    ]