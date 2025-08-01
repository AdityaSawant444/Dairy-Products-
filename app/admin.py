from django.contrib import admin
from .models import  OrderPlaced, Product, Customer, Cart
# Register your models here.

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display: ['id', 'title','discountes_price', 'category', 'product_image']

     
     
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
      list_display: ['id', 'user','locality', 'city',  'state', 'zipcode']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
      list_display: ['id', 'user','product','quantity']      




@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display: ['id', 'user','customer', 'product', 'quantity',  'ordered_date', 'status', 'payment']

   