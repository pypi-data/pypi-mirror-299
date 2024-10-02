from django.urls import path

from . import views

urlpatterns = [
    path("change-logs/", views.change_logs_list, name="change_logs_list"),
    path("change-logs/v<str:version>/", views.change_logs_detail, name="change_logs_detail"),
]
