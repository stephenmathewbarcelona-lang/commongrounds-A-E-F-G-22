from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, FormMixin # Surprised Create and Update are here instead of in above
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from accounts.mixins import RoleRequiredMixin
from accounts.decorators import role_required
from .models import Product, Transaction
from .forms import ProductAssembleForm, TransactionForm

class ProductsListView(ListView):
    model = Product
    template_name = 'productsList.html'
    context_object_name = 'productsList'

    def get_queryset(self): # i only barely understand this insofar i think i get the cook but i need to review this MORE
        queryset = Product.objects.all()

        if self.request.user.is_authenticated:
            return queryset.exclude(owner=self.request.user.profile)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['ownedProducts'] = Product.objects.filter(
                owner=self.request.user.profile
            )
        else:
            context['ownedProducts'] = None

        return context

class ProductDetailView(DetailView, FormMixin): 
    template_name = 'productDetail.html'
    context_object_name = 'product'
    form_class = TransactionForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['form'] = self.get_form()
        
        return context

    def get_success_url(self):
        return reverse('merchstore:cart')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid(): # Okay so looking for alternatives there aren't any its just like this
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path()) # BETTER THAN return redirect('login') because it saves ur location! i really like it :D
        
        if (
            (self.object.owner == self.request.user.profile) or
            (form.cleaned_data['amount'] > self.object.stock)
        ):
            return self.form_invalid(form)
        
        transaction = form.save(commit=False) # EVERYTHING is shouting at me to do this I understand ish whats cook but like can we find a way to not have to do this? why is the form not saved how do i do that
        transaction.product = self.object
        transaction.owner = self.request.user.profile
        
        self.object.stock -= form.cleaned_data['amount']
        self.object.save()
        transaction.save()
        
        return super().form_valid(form)

class ProductCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView): #RoleRequiredMixin made by yours truly will automatically check if a specific role is found in your thing! Also RoleRequiredMixin already has LoginRequiredMixin so does that make LoginRequiredMixin redundant here???   
    model = Product
    template_name = 'productCreate.html'
    form_class = ProductAssembleForm
    required_role = 'Market Seller'
    
    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        return super().form_valid(form)

# wow! a function based implementation. ok i thought this was harder but the more i look at it i think this was easier to make
@login_required
@role_required('Market Seller')
def productUpdateView(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if product.owner != request.user.profile:
        return redirect('merchstore:productsList')
    
    if request.method == 'POST':
        form = ProductAssembleForm(request.POST, request.FILES, instance=product)
        
        if form.is_valid():
            newProduct = form.save(commit=False)
            
            if newProduct.stock == 0:
                newProduct.status = 'Out of stock'
            else:
                newProduct.status = 'Available'
            
            newProduct.save()
            return redirect(newProduct.get_absolute_url())

    else:
        form = ProductAssembleForm(instance=product)
        
    return render(request, 'productUpdate.html', {
        'form': form,
        'product': product,
    })
        
class CartView(ListView):
    model = Transaction
    template_name = 'cart.html'
        
    def get_queryset(self): # Only shows the transactions made by the right user
        return Transaction.objects.filter(owner = self.request.user.profile)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        sortedTransactions = {}
        
        for i in self.get_queryset():
            seller = i.product.owner
            
            if seller not in sortedTransactions:
                sortedTransactions[seller] = []
                
            sortedTransactions[seller].append(i)
        
        context['sortedTransactions'] = sortedTransactions
    
        return context
    

class TransactionslistView(ListView):
    model = Transaction
    template_name = 'transactionsList.html'
        
    def get_queryset(self): # Only shows the transactions from products owned by the user
        return Transaction.objects.filter(product__owner = self.request.user.profile)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        sortedTransactions = {}
        
        for i in self.get_queryset():
            buyer = i.owner
            
            if buyer not in sortedTransactions:
                sortedTransactions[buyer] = []
                
            sortedTransactions[buyer].append(i)
        
        context['sortedTransactions'] = sortedTransactions
    
        return context