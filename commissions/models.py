from django.db import models
from accounts.models import Profile

# Create your models here.
class CommissionType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        
class Commission(models.Model):

    class Status(models.TextChoices):
        OPEN = '1_OPEN', 'Open'
        FULL = '2_FULL', 'Full'
        COMPLETED = '3_COMPLETED', 'Completed'
        DISCONTINUED = '4_DISCONTINUED', 'Discontinued'

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    type = models.ForeignKey(CommissionType, on_delete=models.SET_NULL, null=True)
    maker = models.ForeignKey(Profile, on_delete=models.CASCADE, null = True)
    people_required = models.PositiveIntegerField()
    status = models.CharField(max_length= 20, 
                              choices=Status.choices, 
                              default=Status.OPEN)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['created_on']

class Job(models.Model):
     
    class Status(models.TextChoices):
        OPEN = '1_OPEN', 'Open'
        FULL = '2_FULL', 'Full'

    commission = models.ForeignKey(Commission, on_delete=models.CASCADE)
    role = models.CharField(max_length=255)
    manpower_required = models.PositiveIntegerField()
    status = models.CharField(max_length= 20, 
                              choices=Status.choices, 
                              default=Status.OPEN)

    def __str__(self):
        return f"{self.role} for {self.commission.title}"
    
    class Meta:
        ordering = ['status',
                    '-manpower_required',
                    'role']

class JobApplication(models.Model):
    class Status(models.TextChoices):
        PENDING = '1_PENDING', 'Pending'
        ACCEPTED = '2_ACCEPTED', 'Accepted'
        REJECTED = '3_REJECTED', 'Rejected'
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.CharField(max_length= 20, 
                              choices=Status.choices, 
                              default=Status.PENDING)
    applied_on = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # save the application first

        job = self.job
        accepted_count = JobApplication.objects.filter(
            job=job, status=JobApplication.Status.ACCEPTED
        ).count()

        if accepted_count >= job.manpower_required:
            new_status = Job.Status.FULL
        else:
            new_status = Job.Status.OPEN

        if job.status != new_status:
            job.status = new_status
            job.save()
        
        commission = job.commission
        total_accepted = JobApplication.objects.filter(
            job__commission=commission,
            status=JobApplication.Status.ACCEPTED
        ).count()

        if total_accepted >= commission.people_required:
            new_commission_status = Commission.Status.FULL
        else:
            new_commission_status = Commission.Status.OPEN

        if commission.status != new_commission_status:
            commission.status = new_commission_status
            commission.save()

    def __str__(self):
        return f"{self.applicant} - {self.job}"

    class Meta:
        ordering = [ 'status','-applied_on']