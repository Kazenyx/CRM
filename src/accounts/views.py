from django.http import HttpResponse
from django.urls import reverse_lazy
from django.forms import inlineformset_factory
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import PasswordChangeView, PasswordChangeForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


from .forms import OrderForm, CreateUserForm, CustomerForm
from .models import *
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only
# Create your views here.

@unauthenticated_user
def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')


			messages.success(request, 'Account was created for ' + username)

			return redirect('login')
		

	context = {'form':form}
	return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):
  if request.method == "POST":
      username = request.POST.get('username')
      password = request.POST.get('password')
      
      user = authenticate(request, username=username, password=password)
      
      if user is not None:
        login(request, user)
        return redirect('/')
      else:
        messages.info(request, 'username or password is incorrect')
      
  context = {}
  return render(request, 'accounts/login.html', context)

def logoutUser(request):
  logout(request)
  return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
  orders = Order.objects.all()
  customers = Customer.objects.all()
  
  p = Paginator(orders, 5)
  page = request.GET.get('page')
  pg = p.get_page(page)
  
  total_customers = customers.count()
  total_orders = orders.count()
  pending = orders.filter(status='Pending').count()
  delivered = orders.filter(status='Delivered').count()
  nums = "a" * pg.paginator.num_pages
  
  context = {'orders':orders, 'customers':customers, 'total_customers': total_customers, 'total_orders': total_orders, 'delivered': delivered, 'pending': pending, 'pg': pg, 'nums': nums}
  return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Customers'])
def userPage(request):
  orders = request.user.customer.order_set.all()
  
  total_orders = orders.count()
  pending = orders.filter(status='Pending').count()
  delivered = orders.filter(status='Delivered').count()

  context = {'orders': orders, 'total_orders': total_orders, 'delivered': delivered, 'pending': pending}
  return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
  customer = request.user.customer
  form = CustomerForm(instance=customer)
  
  if request.method == "POST":
    form = CustomerForm(request.POST, request.FILES, instance=customer)
    if form.is_valid():
      form.save()
  
  context = {'form':form}
  return render(request, 'accounts/account_setting.html', context)

def products(request):
  products = Product.objects.all()
  
  p = Paginator(products, 5)
  page = request.GET.get('page')
  products_page = p.get_page(page)
  
  context = {'products':products, 'products_page':products_page}
  return render(request, 'accounts/products.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
  customer = Customer.objects.get(id=pk)
  
  orders = customer.order_set.all()
  total_orders = orders.count()
  
  myFilter = OrderFilter(request.GET, queryset=orders)
  orders = myFilter.qs
  
  context = {"customer": customer, 'orders':orders, 'total_orders': total_orders, 'myFilter': myFilter}
  return render(request, 'accounts/customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
  # OrderFormSet = inlineformset_factory(parent model, child model)
  OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=7)
  customer = Customer.objects.get(id=pk)
  formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
  # form = OrderForm(initial={'customer':customer})
  if request.method == "POST":
    # form = OrderForm(request.POST)
    formset = OrderFormSet(request.POST,instance=customer)
    if formset.is_valid():
      formset.save()
      return redirect('home')

  context = {'formset':formset}
  return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
  
  order = Order.objects.get(id=pk)
  form = OrderForm(instance=order)
  if request.method == "POST":
    form = OrderForm(request.POST, instance=order)
    if form.is_valid():
      form.save()
      return redirect('home')
  
  context = {'form':form}
  return render(request, 'accounts/update.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
  order = Order.objects.get(id=pk)
  if request.method == "POST":
    order.delete()
    return redirect('/')
  
  context = {'item':order}
  return render(request, 'accounts/delete.html', context)

class PasswordsChangeView(PasswordChangeView):
  form_class = PasswordChangeForm
  success_url = reverse_lazy('password_success')
  
  # success_url = reverse_lazy('home')
  
def password_success(request):
  
  context = {}
  return render(request, 'accounts/password_success.html', context)

def passw(request):
  return HttpResponse("shit works with funcs")