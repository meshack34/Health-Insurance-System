from django.urls import path
from .import views

from .views import customer_dashboard
urlpatterns = [
    path('',views.home, name='home'),
    path('register/',views.customerregister, name='register'),
    path('login/',views.user_login, name='login'),
    path('logout/',views.logout, name='logout'),
    path('customers_profile/', views.customers_profile, name='patients_profile'),
    path('customer_dashboard/', views.customer_dashboard, name='customer_dashboard'),
]
