from django.contrib import admin
from .models import Event, EventType, EventSignup

admin.site.register(EventType)
admin.site.register(Event)
admin.site.register(EventSignup)
