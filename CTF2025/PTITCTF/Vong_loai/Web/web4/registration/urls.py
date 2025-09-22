from django.urls import path
from app import views

urlpatterns = [
    path('admin/', views.AdminPage, name='admin'),
    path('', views.SignupPage, name='signup'),
    path('login/', views.LoginPage, name='login'),
    path('home/', views.HomePage, name='home'),
    path('logout/', views.LogoutPage, name='logout'),    
]