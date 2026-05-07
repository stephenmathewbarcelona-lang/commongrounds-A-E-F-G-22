from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from accounts.models import Profile       
from accounts.mixins import RoleRequiredMixin  
from .models import Event, EventType, EventSignup

class BaseSignupView(View):
    def post(self, request, *args, **kwargs):
        event = self.get_event()
        user = request.user
        if not self.check_capacity(event):
            return redirect(self.get_redirect_url(event))
        if not self.check_ownership(event, user):
            return redirect(self.get_redirect_url(event))
        self.create_signup(event, user)
        return redirect(self.get_redirect_url(event))

    def get_event(self):
        return get_object_or_404(Event, pk=self.kwargs.get('pk'))

    def check_capacity(self, event):
        return event.eventsignup_set.count() < event.capacity

    def check_ownership(self, event, user):
        if not user.is_authenticated: return True
        return not event.organizer.filter(id=user.profile.id).exists()

    def create_signup(self, event, user):
        raise NotImplementedError()

    def get_redirect_url(self, event):
        return reverse('localevents:event_list')

class EventListView(ListView):
    model = Event
    template_name = 'localevents/event_list.html'
    context_object_name = 'all_events'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            created = Event.objects.filter(organizer=profile)
            signed_up = Event.objects.filter(eventsignup__user_registrant=profile)
            context['created_events'] = created
            context['signed_up_events'] = signed_up
            context['all_events'] = Event.objects.exclude(id__in=created).exclude(id__in=signed_up)
        return context

class EventDetailView(DetailView):
    model = Event
    template_name = 'localevents/event_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.object
        user = self.request.user
        is_owner = user.is_authenticated and event.organizer.filter(id=user.profile.id).exists()
        count = event.eventsignup_set.count()
        context['is_owner'] = is_owner
        context['is_full'] = count >= event.capacity
        context['signup_count'] = count
        context['can_signup'] = not is_owner and not context['is_full']
        return context

class EventCreateView(RoleRequiredMixin, CreateView):
    model = Event
    template_name = 'localevents/event_form.html'
    required_role = "Event Organizer" 
    fields = ['title', 'category', 'event_image', 'description', 'location', 'start_time', 'end_time', 'capacity', 'status']
    success_url = reverse_lazy('localevents:event_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('admin:login')
        return super().dispatch(request, *args, **kwargs)
    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.organizer.add(self.request.user.profile)
        return response

class EventUpdateView(RoleRequiredMixin, UpdateView):
    model = Event
    template_name = 'localevents/event_form.html'
    required_role = "Event Organizer"
    fields = ['title', 'category', 'event_image', 'description', 'location', 'start_time', 'end_time', 'capacity', 'status']

    def form_valid(self, form):
        event = form.save(commit=False)
        if event.eventsignup_set.count() >= event.capacity:
            event.status = "Full"
        else:
            if event.status == "Full":
                event.status = "Available"
        event.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('localevents:event_detail', kwargs={'pk': self.object.pk})

class EventSignupView(BaseSignupView):
    def get(self, request, *args, **kwargs):
        event = self.get_event()
        if request.user.is_authenticated:
            return self.post(request, *args, **kwargs)
        return render(request, 'localevents/signup_form.html', {'event': event})

    def create_signup(self, event, user):
        if user.is_authenticated:
            EventSignup.objects.get_or_create(event=event, user_registrant=user.profile)
        else:
            name = self.request.POST.get('new_registrant')
            if name:
                EventSignup.objects.create(event=event, new_registrant=name)

    def get_redirect_url(self, event):
        return reverse('localevents:event_detail', kwargs={'pk': event.pk})
