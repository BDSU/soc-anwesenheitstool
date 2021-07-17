from django.urls import path
from . import views
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path("details/<int:pk>/", staff_member_required(views.MeetingDetailView.as_view()),
         name="meeting_details"),
    path("checkin/<uuid:slug>", views.checkin_view, name="meeting_checkin"),
    path("update/<int:pk>/", views.update_meeting, name="update_meeting"),
    path("delete/<int:pk>/", views.delete_meeting, name="delete_meeting"),
    path('export/<int:pk>/', views.export, name='export'),
]
