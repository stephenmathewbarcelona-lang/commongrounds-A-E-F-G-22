from .models import Profile
from django.urls.base import reverse_lazy
from .forms import ProfileUpdateForm
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView

# Create your views here.

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'profile_update.html'
    form_class = ProfileUpdateForm

    def get_object(self, queryset=None):
     return self.request.user.profile

    def get_success_url(self):
        return reverse_lazy('commissions:commissions-list') 