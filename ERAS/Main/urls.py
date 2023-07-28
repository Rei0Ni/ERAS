from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.home, name='Home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('event/<str:id>/', views.ViewEvent, name='View Event Data'),
    path('create/event/', views.CreateEvent, name='Event Creation'),
    path('event/<str:id>/update/', views.UpdateEvent, name='Event Update'),
    path('event/<str:id>/delete/', views.DeleteEvent, name="Event Deletion"),
    path('event/<str:event_id>/ticket/create/', views.CreateTicketUI, name="create new event ticket"),
    path('event/<str:event_id>/ticket/<str:ticket_id>/', views.ViewTicket, name="View Ticket Info"),
    path('event/<str:event_id>/staff/add/', views.AddStaffToEvent, name="add staff to event"),
    path('event/<str:event_id>/staff/remove/', views.RemoveEventStaff, name='remove staff from event')
]
