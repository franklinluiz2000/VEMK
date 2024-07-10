from django.urls import path
from . import views

urlpatterns = [    
    path('company_list/', views.company_list, name='companys'),
    path('company_data/<str:id>/', views.company_data, name="company_data"),
    path('delete_company/<str:id>', views.delete_company, name='delete_company'),
    path('delete_product//<str:id>', views.delete_product, name='delete_product'),
    path('product_view/<str:id>', views.product_view, name='product_view'),

]
