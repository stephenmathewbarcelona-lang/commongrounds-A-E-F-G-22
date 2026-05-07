from django.db import models
from accounts.models import Profile
from django.urls import reverse

class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Product(models.Model): # FOR ETHAN: Remember that 'blank=True, null=True' exists to make something OPTIONAL.
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=999)
    stock = models.PositiveIntegerField(default=0)

    statusChoices = [
        ('Available', 'Available'),
        ('On sale', 'On sale'),
        ('Out of stock', 'Out of stock'),
    ]
    status = models.CharField(max_length=255, choices=statusChoices, default=statusChoices[0])
    
    productType = models.ForeignKey(
        ProductType,
        on_delete = models.SET_NULL,
        null=True,
        related_name = 'product'
    )
    
    owner = models.ForeignKey(
        Profile,
        on_delete = models.CASCADE,
        related_name = 'product',
        null=True,
        blank=True,
    )
    
    def get_absolute_url(self):
        return reverse('merchstore:merchstore_detail', args=[self.pk])
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Transaction(models.Model):
    amount = models.PositiveIntegerField(default=0)
    createdOn = models.DateTimeField(auto_now_add=True)
    
    statusChoices = [
        ('On cart', 'On cart'),
        ('To pay', 'To pay'),
        ('To ship', 'To ship'),
        ('To receive', 'To receive'),
        ('Delivered', 'Delivered'),
    ]
    status = models.CharField(max_length=255, choices=statusChoices, default=statusChoices[0])

    owner = models.ForeignKey(
        Profile,
        on_delete = models.SET_NULL,
        null=True,
        related_name = 'transaction'
    )
    
    product = models.ForeignKey(
        Product,
        on_delete = models.CASCADE,
        related_name = 'transaction'
    )
    
    def __str__(self):
        return str(self.amount) + " of " + str(self.product) + " for " + str(self.buyer)
