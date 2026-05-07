from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    """
    Profile model required for Organizer and UserRegistrant relationships.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, default="Attendee") # e.g., "Event Organizer"

    def __str__(self):
        return self.user.username

class EventType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        # Types should be sorted by name in ascending order
        ordering = ['name']

    def __str__(self):
        return self.name

class Event(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Full', 'Full'),
        ('Done', 'Done'),
        ('Cancelled', 'Cancelled'),
    ]

    title = models.CharField(max_length=255)
    
    # Category: sets to NULL when deleted
    category = models.ForeignKey(
        EventType, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    # Organizer: Many-to-many relationship to Profile.
    # Note: M2M relationships automatically remove the link record when a Profile is deleted.
    organizer = models.ManyToManyField(Profile)
    
    event_image = models.ImageField(upload_to='events/')
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    # Event capacity: natural number (PositiveIntegerField)
    capacity = models.PositiveIntegerField()
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='Available'
    )
    
    # Only gets set when the model is created
    created_on = models.DateTimeField(auto_now_add=True)
    
    # Always updates on last model update
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        # Events should be sorted by the date it was created, in descending order
        ordering = ['-created_on']

    def __str__(self):
        return self.title
    
    @property
    def current_signup_count(self):
        # This counts all EventSignup records linked to this specific event
        return self.eventsignup_set.count()

class EventSignup(models.Model):
    # Event: cascaded deletion
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    
    # UserRegistrant: cascaded deletion, set when registrant is logged in
    user_registrant = models.ForeignKey(
        Profile, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    
    # NewRegistrant: set when registrant is not logged in
    new_registrant = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        registrant = self.user_registrant.user.username if self.user_registrant else self.new_registrant
        return f"{registrant} signup for {self.event.title}"
