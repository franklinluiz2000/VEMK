from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.contrib.messages import constants
from django.conf import settings
from .utils import password_is_valid, email_html
from .models import UserActivation
from hashlib import sha256
from django.core.mail import send_mail
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
            activation = UserActivation(token=token, user=user)
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
    token = get_object_or_404(UserActivation, token=token)

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

