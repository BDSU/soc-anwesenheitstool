from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path("update/<int:pk>/", views.update_meeting, name="update_meeting"),
    path("delete/<int:pk>/", views.delete_meeting, name="delete_meeting"),
    ]