from django.urls import path, include
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeView

from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    
    path('', views.home, name='home'),
    path('user/', views.userPage, name='user-page'),
    
    path('account/', views.accountSettings, name='account'),
    
    path('products/', views.products, name='products'),
    path('customer/<str:pk>/', views.customer, name='customer'),
    
    path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),

    path('password/', views.PasswordsChangeView.as_view(template_name="accounts/change-password.html"), name="password"),
    path('password_success', views.password_success, name="password_success"),
    # path('password/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('account:password_change_done')),name="password"),
    # path('password-change/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('account:password_change_done')), name='password_change'),
    
    # path('password_change/', auth_views.PasswordChangeView.as_view(
    #     success_url=reverse_lazy('account:password_change_done')
    # ), name='password_change'),
    # path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

]
  
