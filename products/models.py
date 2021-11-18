from django.db import models


# Create your models here.
class Category(models.Model):
  
    class Meta:
        verbose_name_plural = 'Categories'
# this is to correct the plural
# conversion of 'Category(...)'. See the admin page

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    # null and blank true allow the variable to be optional

    # creating a string method, with data model = self /what does it do?
    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


# Model for the product
class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    # when changing this part above, it changes the structure of the model.
    # ... Therefore needs to run migrations
    # (test) python3 manage.py makemigrations --dry-run
    # (run migration) python3 manage.py makemigrations
    # (it shows the migrations that will be run):
    # ... python3 manage.py migrate --plan

    def __str__(self):
        return self.name
