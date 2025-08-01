
from django.db.models import Count
from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.views import View
from .models import Product, Customer, Cart,OrderPlaced
from .forms import CustomerProfileForm, CustomerRegistrationForm, MyPasswordResetForm
from django.contrib import messages
from .models import Customer
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, "app/home.html")

def about(request):
    return render(request, "app/about.html")

def contact(request):
    return render(request, "app/contact.html")


class CategoryView(View):
    def get(self,request,val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request,"app/category.html",locals())

class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request,"app/category.html",locals())


class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        return render(request,"app/productdetail.html",locals())
    
class CustomerRegistrationView(View):
    def get(self,request):
            form = CustomerRegistrationForm()
            return render(request, 'app/customerregistration.html',locals())
    
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! User Registration Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request, 'app/customerregistration.html',locals())
    
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request,"app/profile.html",locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            
            reg = Customer(user=user,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save() 
            messages.success(request,"Congratulations! Profile Save Successfully")     
        else:         
            messages.warning(request,"Invalid Input Data")
        return render(request,"app/profile.html",locals())
    
def address(request):
    add = Customer.objects.filter(user=request.user)    
    return render(request,"app/address.html",locals())

class UpdateAddress(View):
    def get(self,request,pk):
       add = Customer.objects.get(pk=pk)
       form = CustomerProfileForm(instance=add)
       return render(request,"app/updateAddress.html",locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        return render(request,"app/updateAddress.html",locals())

@login_required
@require_POST
def add_to_cart(request):
    user = request.user
    product_id = request.POST.get('prod_id')
    product = Product.objects.get(id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('showcart')

def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discountes_price 
        amount = amount + value 
        totalamount = amount + 40
    return render(request, 'app/addtocart.html',locals())


class checkout(View):
    def get(self,request):
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
         value = p.quantity * p.product.discountes_price 
         famount = famount + value 
         totalamount = famount + 40
        return render(request, 'app/checkout.html',locals())



def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) &Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
         value = p.quantity * p.product.discountes_price 
         amount = amount + value 
         totalamount = amount + 40
        
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
            
        }
        return JsonResponse(data) 
    

def minus_cart(request):
     if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) &Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
         value = p.quantity * p.product.discountes_price 
         amount = amount + value 
         totalamount = amount + 40
        
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
            
        }
        return JsonResponse(data) 
     

def remove_cart(request):
      if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.filter(Q(product=prod_id) &Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
         value = p.quantity * p.product.discountes_price 
         amount = amount + value 
         totalamount = amount + 40
        
        data={
            'amount':amount,
            'totalamount':totalamount
            
        }
        return JsonResponse(data) 
      
def place_order(request):
    if request.method == 'POST':
        user = request.user
        Cart.objects.filter(user=user).delete()
        messages.success(request, "Your order has been confirmed.")
        return redirect('showcart')  
   

def placeorder(request):
     messages.success(request, "Your order has been confirmed.")
     return redirect('order_confirmed')  

def order_confirmed(request):
    return render(request, 'order_confirmed.html')