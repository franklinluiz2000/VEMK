from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from authentication.utils import company_valid_data
from .models import Company, Product, Category
from django.contrib import messages


@login_required(login_url='/auth/login/')
def company_list(request):
    
    if request.method == "GET":
        companys = Company.objects.filter(linked_user=request.user)
        return render(request, 'companys.html', {'companys': companys})

    elif request.method == "POST":
        
        name_company = request.POST.get('name_company')
        cnpj = request.POST.get('cnpj')
        state = request.POST.get('state')
        address = request.POST.get('address')
        cep = request.POST.get('cep')
        city = request.POST.get('city')
        phone = request.POST.get('phone')
        chosen_plan = request.POST.get('plan')
        image = request.POST.get('image')

        if not  company_valid_data(request, name_company, cnpj, phone, address, cep, city, state):
            return redirect('/company_list')              
     
    try:    
        
        company = Company.objects.create(name_company=name_company, cnpj=cnpj, phone=phone, address=address, cep=cep, city=city, state=state, chosen_plan=chosen_plan, linked_user=request.user, image=image)
        company.save()

        messages.add_message(request, messages.constants.SUCCESS, 'Sua empresa foi cadastrada com sucesso')
        return redirect('/company_list')
   
    except:
        messages.add_message(request, messages.constants.ERROR, 'Erro interno do sistema')
        return redirect('/company_list/')


@login_required(login_url='/auth/login/')
def company_data(request, id):
    company = get_object_or_404(Company, id=id)
    if not company.linked_user == request.user:
        messages.add_message(request, messages.constants.ERROR, 'Esse empresa não é sua')
        return redirect('/company_data/')
        
    if request.method == "GET":
        products = Product.objects.filter(linked_company=company)
        return render(request, 'company_data.html', {'company': company, 'products': products})

        # return render(request, 'company_data.html', {'company': company})
    
    elif request.method == "POST":
        product_name = request.POST.get('product_name')
        category = request.POST.get('category')
        price = request.POST.get('price')
        description = request.POST.get('description')
        img=request.POST.get('image')
  
   

    try: 
        category_object = Category.objects.filter(category=category).first()
        if category_object is None:
            category_object = Category.objects.create(category=category)
            category_object.save()          

        product = Product.objects.create(product_name=product_name, category=category_object, price=price, description=description, linked_company=company, img=img)
        product.save()

        messages.add_message(request, messages.constants.SUCCESS, f"O produto {product_name} foi cadastrado com sucesso!")       
        return redirect(f'/company_data/{company.id}')

    except:
        messages.add_message(request, messages.constants.ERROR, "ERRO interno do sistema! Por favor entre em contato com o administrador")
        return redirect(f'/company_data/{company.id}')