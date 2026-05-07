from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.urls.base import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from .models import Commission, CommissionType, Job, JobApplication
from accounts.mixins import RoleRequiredMixin
from .forms import CommissionForm, JobApplicationForm, JobFormSet, JobFormSetUpdate

# Create your views here.
class CommissionRequestsListView(ListView):
    model = Commission
    template_name = "commissions_list.html"
    context_object_name = "commissions"

    def get_queryset(self):
        return Commission.objects.order_by("status", "-created_on")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            user_profile = self.request.user.profile
            
            user_commissions = Commission.objects.filter(
                maker=user_profile
            ).order_by("status", "-created_on")
            
            applied_commissions = Commission.objects.filter(
                job__jobapplication__applicant=user_profile
            ).distinct().order_by("status", "-created_on")

            excluded_ids = set(user_commissions.values_list("id", flat=True)) | \
                           set(applied_commissions.values_list("id", flat=True))

            context["user_commissions"] = user_commissions
            context["applied_commissions"] = applied_commissions
            context["commissions"] = context["commissions"].exclude(id__in=excluded_ids)
        
        return context

class CommissionRequestsDetailView(DetailView):
    model = Commission
    template_name = "commissions_detail.html"
    context_object_name = "commission"
    form_class = JobApplicationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        commission = self.get_object()
        jobs = commission.job_set.all()
        context["jobs"] = jobs

        if self.request.user.is_authenticated:
            user_profile = self.request.user.profile

            for job in jobs:
                job.accepted_count = JobApplication.objects.filter(
                    job=job, status="2_ACCEPTED"
                ).count()
                job.pending_status = JobApplication.objects.filter(
                    job=job, applicant=user_profile,
                    status="1_PENDING"
                ).exists()
                job.accepted_status = JobApplication.objects.filter(
                    job=job, applicant=user_profile, status="2_ACCEPTED"
                ).exists()
                job.rejected_status = JobApplication.objects.filter(
                    job=job, applicant=user_profile,
                    status="3_REJECTED"
                ).exists()
                job.is_full = job.accepted_count >= job.manpower_required
                job.open_manpower = job.manpower_required - job.accepted_count

            context["is_owner"] = commission.maker == user_profile

        return context
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('commissions:commissions-detail', pk=kwargs['pk'])

        commission = self.get_object()
        user_profile = request.user.profile
        job_id = request.POST.get('job_id')

        if job_id:
            job = get_object_or_404(Job, pk=job_id, commission=commission)

            accepted_count = JobApplication.objects.filter(
                job=job, status=JobApplication.Status.ACCEPTED
            ).count()
            is_full = accepted_count >= job.manpower_required
            already_applied = JobApplication.objects.filter(
                job=job, applicant=user_profile
            ).exists()

            if not is_full and not already_applied:
                form_data = {
                    'job': job.pk,
                    'applicant': user_profile.pk,
                    'status': JobApplication.Status.PENDING,
                }
                form = JobApplicationForm(data=form_data)

                if form.is_valid():
                    form.save()
        
        return redirect('commissions:commissions-detail', pk=commission.pk)

    
    def get_success_url(self):
        return reverse_lazy('commissions:commissions-detail', 
                            kwargs={'pk': self.object.pk})


class CommisionRequestCreateView(RoleRequiredMixin, CreateView):
    model = Commission
    template_name = "commissions_create.html"
    form_class = CommissionForm
    required_role = 'Commission Maker'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['job_formset'] = JobFormSet(self.request.POST)
        else:
            context['job_formset'] = JobFormSet()
        return context

    def form_valid(self, form):
        job_formset = JobFormSet(self.request.POST)

        if job_formset.is_valid():
            form.instance.maker = self.request.user.profile
            self.object = form.save()

            job_formset.instance = self.object
            job_formset.save()

            return redirect(self.get_success_url())

        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('commissions:commissions-list') 




class CommisionRequestUpdateView(RoleRequiredMixin, UpdateView):
    model = Commission
    template_name = "commissions_update.html"
    form_class = CommissionForm
    required_role = 'Commission Maker'

    def test_func(self):
        # Only the owner of the commission can update it
        return self.get_object().maker == self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['job_formset'] = JobFormSetUpdate(self.request.POST, instance=self.object)
        else:
            context['job_formset'] = JobFormSetUpdate(instance=self.object)
        return context

    def form_valid(self, form):
        job_formset = JobFormSetUpdate(self.request.POST, instance=self.object)

        if job_formset.is_valid():
            self.object = form.save()
            job_formset.save()

            # If every job is full, mark the commission as full
            jobs = self.object.job_set.all()
            if jobs.exists() and all(job.status == Job.Status.FULL for job in jobs):
                self.object.status = Commission.Status.FULL
                self.object.save()

            return redirect(self.get_success_url())

        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('commissions:commissions-detail', 
                            kwargs={'pk': self.object.pk})

