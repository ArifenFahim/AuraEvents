from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='home'),
    path('register/', views.register, name='register'),
    path('create/', views.create_event, name='create_event'),
    path('book/<int:event_id>/', views.book_event, name='book_event'),
    path('booked/', views.booked_events, name='booked_events'),
]
