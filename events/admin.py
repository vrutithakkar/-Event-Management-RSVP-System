from django.contrib import admin
from .models import Event, RSVP


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'location',
        'event_date',
        'event_time',
        'created_by'
    )

    search_fields = (
        'title',
        'location'
    )

    list_filter = (
        'event_date',
        'location'
    )


@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'event',
        'joined_at'
    )