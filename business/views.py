from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from authentication.utils import company_valid_data
from .models import Company, Product, Category
from django.contrib import messages
from .forms import ProductForm, CompanyForm


@login_required(login_url='/auth/login/')
def company_list(request):    
    companys = Company.objects.filter(linked_user=request.user)
    if request.method == "GET":
        form = CompanyForm()       
        context = {
            'companys': companys,
            'form': form
        }
        return render(request, template_name="companys.html", context=context)        
        
   
    elif request.method == "POST":
        form = CompanyForm(request.POST, request.FILES)       
        if form.is_valid(): 
            company = form.save(commit=False)
            company.linked_user = request.user     # associa a empresa ao usuário logado    
            form.save()
            messages.add_message(request, messages.constants.SUCCESS, f"Parabéns {request.user}! Você acabou de cadastrar sua empresa!")
        else:
            form = CompanyForm() 
            messages.add_message(request, messages.constants.ERROR, "ERRO interno do sistema!")
        context = {
            'form': form,    
            'company': company              
        }

        return render(request, 'companys.html', context=context)
    

     

@login_required(login_url='/auth/login/')
def company_data(request, id=None):

    company = get_object_or_404(Company, id=id)
    product = Product()
    teste = request.POST.get('price')

    # Caso a requisão seja get mostrar os produtos cadastrados na tela
    if request.method == "GET":
            form = ProductForm()
            products = Product.objects.filter(linked_company=company.id)
            print(products)
            context = {
                'products': products,
                'form': form,
                'company': company,
            }
            return render(request, template_name="company_data.html", context=context)
    
    # Se a requisição for post validar o formulario      
    elif request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            print("form valido")
            product = form.save(commit=False)
            product.linked_company = company    # associa a empresa ao usuário logado    
            form.save()
            messages.add_message(request, messages.constants.SUCCESS, f"Parabéns, {request.user}! O produto foi adicionado com sucesso!")
            return redirect(f"/company_data/{company.id}")
    else:
        form = ProductForm()
        messages.add_message(request, messages.constants.ERROR, "ERRO interno do sistema!")
    context = {
        'company': company,
        'form': form,
        
    } 

    return render(request, 'company_data.html', context=context)





def delete_company(request, id=None):

    company = get_object_or_404(Company, id=id)

    if company:
        company.delete()
        messages.add_message(request, messages.constants.SUCCESS, f"A empresa {company.name_company} foi removida com sucesso! Volte quando quiser!")
    elif not company:
        messages.add_message(request, messages.constants.ERROR, "A Empresa não foi encontrada!")    

    return redirect("/company_list/")


def delete_product(request, id=None):

    product = get_object_or_404(Product, id=id)

    if product:
        product.delete()
        messages.add_message(request, messages.constants.SUCCESS, f"O {product.product_name} foi removido com sucesso!")
    elif not product:
        messages.add_message(request, messages.constants.ERROR, "O produto não foi encontrado!")    

    return redirect("/company_data")


def product_view(request, id=None):
    product = get_object_or_404(Product, id=id)
    context = {
        'product': product
    }
    if product:
        return render(request, template_name="product_view.html", context=context)
    else:
        messages.add_message(request, messages.constants.ERROR, "O produto não pode ser encontrado")
        return redirect("/company_data")
