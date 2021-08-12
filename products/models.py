from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_lenght=254)
    friendly_name = models.CharField(max_lenght=254, null=True, blank=True)
    # null and blank true allow the variable to be optional

    # creating a string method, with data model = self
    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


# Model for the product
class Products(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name