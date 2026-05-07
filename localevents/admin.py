from django.contrib import admin
from .models import Event, EventType, Profile, EventSignup

admin.site.register(Profile)
admin.site.register(Event)
admin.site.register(EventType)
admin.site.register(EventSignup)
