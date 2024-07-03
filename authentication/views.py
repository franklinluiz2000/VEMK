from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.contrib.messages import constants
from django.conf import settings
from .utils import company_valid_data, user_valid_data, email_html
from .models import Activation, ActivationCompany, Company
from hashlib import sha256
import os

def home(request):
    name = request.user
    return HttpResponse(f"<h1>Página Inicial {name}</h1>")


def register(request):
    if request.method == "GET":
         return render(request, 'register.html')
    
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        confirm_password = request.POST.get('confirm_password')
    
        if not user_valid_data(request, username, email, password, confirm_password):
            return redirect('/auth/register')               
        
        try:
            user = User.objects.create_user(username=username,email=email, password=password, is_active=False)
            user.save()

            token = sha256(f"{username}{email}".encode()).hexdigest()
            activation = Activation(token=token, user=user)
            activation.save()

            path_template = os.path.join(settings.BASE_DIR, 'authentication/templates/emails/confirm_register.html')
            email_html(path_template, 'Cadastro confirmado', [email,], username=username, activation_link=f"127.0.0.1:8000/auth/activate_account/{token}")

            messages.add_message(request, constants.SUCCESS, 'Acabamos de mandar um link pra você, verifique a caixa de entrada do seu email e ative sua conta')
            return redirect('/auth/login')        
        
        except:
            messages.add_message(request, constants.ERROR,"ERRO interno do sistema!")
            return redirect('/auth/register')
    
    return render(request, 'register.html', status=200)


def login(request):
    if request.user.is_authenticated:
        return redirect('/')
        
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == "" or password == "":
            messages.add_message(request, constants.ERROR, 'Preencha os dois campos e faça o login')
            return redirect('/auth/login')
        user = auth.authenticate(username=username, password=password)

        if not user:
            messages.add_message(request, messages.constants.ERROR, 'Username ou senha inválidos')
            return redirect('/auth/login')
        else:
            auth.login(request, user)
            return redirect('/')
    pass

def logout(request):
    auth.logout(request)
    return redirect('/auth/login')

def activate_account(request, token):
    token = get_object_or_404(Activation, token=token)

    if token.active:
        messages.add_message(request, constants.WARNING, 'Essa token já foi usado')
        return redirect('/auth/login')
    
    
    user = User.objects.get(username=token.user.username)
    user.is_active = True
    user.save()
    token.active = True
    token.save()
    messages.add_message(request, constants.SUCCESS, f'Parabéns, {user.username} sua conta foi ativa com sucesso')
    
    return redirect('/auth/login')


################### EMPRESA #######################

def company_register(request):

    if request.method == 'GET':
        redirect('/auth/company_register')

    elif request.method == 'POST':
        name = request.POST.get('name')
        cnpj = request.POST.get('cnpj')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        cep = request.POST.get('cep')
        city = request.POST.get('city')
        plan = request.POST.get('plan')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # validações dos campos de entrada
        if not  company_valid_data(request, name, cnpj, phone, email, address, cep, city, plan, password, confirm_password):
            return redirect('/auth/company_register')     
         
        try:
            company = Company.objects.create(name=name, cnpj=cnpj, phone=phone, email=email, address=address, cep=cep, city=city, chosen_plan=plan)  

            company.save()

            token = sha256(f"{name}{email}".encode()).hexdigest()
            print("active ainda ")
            activation = ActivationCompany(token=token, company=company) 
            print("meio")                    
            activation.save()
            print("active ok")
            path_template = os.path.join(settings.BASE_DIR, 'authentication/templates/emails/confirm_register_copmany.html')
            email_html(path_template, 'Cadastro confirmado', [email,], name=name, activation_link=f"127.0.0.1:8000/auth/activate_account_company/{token}")

            messages.add_message(request, constants.SUCCESS, 'Acabamos de mandar um link pra você, verifique a caixa de entrada do seu email e ative sua conta')
            return render(request, 'company_login.html', status=200)    
        except:
            messages.add_message(request, constants.ERROR,"ERRO interno do sistema!")
            return render(request, 'company_register.html', status=200)    

    return render(request, 'company_register.html', status=200)
    

def company_login(request):
    return render(request, "company_login.html", status=200)
def company_logout(request):
    pass








def activate_account_company(request, token):
    token = get_object_or_404(ActivationCompany, token=token)

    if token.active:
        messages.add_message(request, constants.WARNING, 'Essa token já foi usado')
        return redirect('/auth/company_login')
            
    company = Company.objects.get(name=token.company.name)
    company.active = True
    company.save()
    token.active = True
    token.save()
    messages.add_message(request, constants.SUCCESS, f'Parabéns, {company.name} sua conta foi ativa com sucesso')
    
    return redirect('/')
   
    