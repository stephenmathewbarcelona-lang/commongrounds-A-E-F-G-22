from django.db import models

# Create your models here.

class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['name']

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    producttype = models.ForeignKey(
        ProductType,
        on_delete = models.CASCADE,
        related_name = 'product'
    )
    price = models.DecimalField(decimal_places=2, max_digits=99999999)

    class Meta:
        ordering = ['name']