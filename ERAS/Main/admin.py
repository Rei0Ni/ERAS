from django.contrib import admin
from .models import Event, Ticket

# Register your models here.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "event_id", "location",)
    search_fields = ["title", "user", "event_id"]
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("user", "ticket_id", "attended", )
    search_fields = ["Event", "user", "ticket_number"]