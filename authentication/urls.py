from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('activate_account/<str:token>/', views.activate_account, name="activate_account"),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('company_register/', views.company_register, name='company_register'),
    path('company_login/', views.company_login, name='company_login'),
    path('company_logout/', views.company_logout, name='company_logout'),
]
