from django.urls import path
from . import views

urlpatterns = [    
    path('company_list/', views.company_list, name='companys'),
    path('company_data/<str:id>/', views.company_data, name="company_data"),   

]
