from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.contrib.messages import constants
from django.conf import settings
from .utils import password_is_valid, email_html, valid_phone_number, is_valid_cep, validate_cnpj, validate_email_with_domain
from .models import Activation, Company
from hashlib import sha256
import os

def register(request):
    if request.method == "GET":
         return render(request, 'register.html')
    
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        confirm_password = request.POST.get('confirm_password')
    
        if not password_is_valid(request, password, confirm_password):
            return redirect('/auth/register')       

        # Verificando se o usuário ou email já existe
        verifyusername = User.objects.filter(username=username).first()
        verifyemail =User.objects,filter(email=email)
        if verifyusername is not None:
            messages.add_message(request, messages.constants.ERROR, 'Usuário já existe')
            return redirect('/auth/register')          
        if verifyemail is not None:
            messages.add_message(request, constants.ERROR, 'Este email já esta cadastrado!')
            return redirect('auth/register')

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
        # if (len(name.strip()) == 0) or (len(cnpj.strip()) == 0) or (len(phone.strip()) == 0) or (len(email.strip()) == 0) or (len(address.strip()) == 0 or (len(city.strip()) == 0)or (len(plan.strip()) == 0)):
        #     messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
        #     return redirect('/auth/company_register')

        if not password_is_valid(request, password, confirm_password):
            return redirect('/auth/company_register')
        
      
        if not validate_email_with_domain(email):
            messages.add_message(request, constants.ERROR,"Digite um email válido")
            return redirect('/auth/company_register')
        
        # if cnpj.isnumeric():
        #     if not validate_cnpj(cnpj):
        #         messages.add_message(request, constants.ERROR,"Digite um cnpj válido.")
        #         return redirect('/auth/company_register')
        # else:
        #     messages.add_message(request, constants.ERROR, "Digite números no campo ")
        #     return redirect('/auth/company_register')
        

        # if phone.isnumeric():
        #     if not valid_phone_number(phone):
        #         messages.add_message(request, constants.ERROR, "Digite um número de telefone válido")
        #         return redirect('/auth/company_register')
        # else:
        #     messages.add_message(constants.ERROR, "Digite um número de telefone válido")
        #     return redirect('/auth/company_register')

        # if cep.isnumeric():
        #     if not is_valid_cep(cep):
        #         messages.add_message(request, constants.ERROR, "Digite um CEP válido")
        #         return redirect('/auth/company_register')
        # else: 
        #     messages.add_message(request,  constants.ERROR, 'Digite números no campo de CEP')
        

        verifyName = Company.objects.filter(name=name)
        verifyCnpj = Company.objects.filter(cnpj=cnpj)
        verifyEmail = Company.objects.filter(email=email)

        # if len(name) < 3:
        #     messages.add_message(request, constants.ERROR, "O nome do usuário é preciso no mínimo 3 caracteres")
        # elif verifyName.exists:
        #     messages.add_message(request, constants.ERROR, "Este usuário já existe")
        #     return redirect('/auth/company_register')
        # elif verifyCnpj.exists:
        #     messages.add_message(request, constants.ERROR, "Este cnpj já está cadastrado")
        #     return redirect('/auth/company_register')
        # elif verifyEmail.exists:
        #     messages.add_message(request, constants.ERROR, "Este email já está sendo usado por outro usuário")
        #     return redirect('/auth/company_register')

        company = Company.objects.create(name=name, cnpj=cnpj, phone=phone, email=email, address=address, cep=cep, city=city, chosen_plan=plan)
        company.save

        return render(request, 'company_login.html', status=200)    


    return render(request, 'company_register.html', status=200)
    

def company_login(request):
    pass

def company_logout(request):
    pass