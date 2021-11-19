from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('int:<product_id>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
]
# above, 'int: ' is necessary because otherwise when navigating to 'add/', this can be considered the id. like id=add
