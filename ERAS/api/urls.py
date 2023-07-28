from django.urls import include, path
from . import views

urlpatterns = [
    path('accounts/login/', views.api_login, name='login'),
    path('accounts/logout/', views.api_logout, name='logout'),
    path('accounts/register/', views.api_register, name="register new user"),
    path('event/<str:event_id>/ticket/create/', views.CreateTicketAPI, name="create ticket"),
    path('tickets/', views.get_tickets, name="get user tickets"),
    path('attendance/record/', views.record_Attendance, name="record attendance for attendee")
]