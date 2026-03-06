from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Commission, CommissionType

# Create your views here.
class CommissionRequestsListView(ListView):
    model = CommissionType
    template_name = "commissions_list.html"
    context_object_name = "commission_types"

class CommissionRequestsDetailView(DetailView):
    model = Commission
    template_name = "commissions_detail.html"
    context_object_name = "commission"