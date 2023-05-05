from django.urls import path
from . import views

urlpatterns = [
    path("event/", views.calendar_test),
    path("schedule/", views.schedule)
]
