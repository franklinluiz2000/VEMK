from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('activate_account/<str:token>/', views.activate_account, name="activate_account"),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout')
]
