from django.urls import path
from . import views

urlpatterns = [
    path("schedule/", views.schedule),
    path("register/", views.register),
    path("signin/", views.signin),
    path("update/", views.update_settings),
    path("confirm/", views.post_tasks),
    path("logout/", views.log_out),
]
