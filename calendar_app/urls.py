from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_calendar, name='calendar'),
    path('add/', views.add_event, name='add_event'),
]
