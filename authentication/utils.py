from django.contrib import messages
from django.contrib.messages import constants
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth.models import User
from business.models import Company
import re
import phonenumbers
import requests

# validando senhas
def password_is_valid(request, password, confirm_password):
    if len(password) < 6:
        messages.add_message(request, constants.ERROR, 'Sua senha deve conter 6 ou mais caractertes')
        return False
   
    if not password == confirm_password:
        messages.add_message(request, constants.ERROR, 'As senhas não coincidem!')
        return False
    
    if not re.search('[A-Z]', password):
        messages.add_message(request, constants.ERROR, 'Sua senha não contem letras maiúsculas')
        return False

    if not re.search('[a-z]', password):
        messages.add_message(request, constants.ERROR, 'Sua senha não contem letras minúsculas')
        return False

    if not re.search('[1-9]', password):
        messages.add_message(request, constants.ERROR, 'Sua senha não contém números')
        return False

    return True

# validando número de telefone
def valid_phone_number(phone_number):  
    if not phone_number.isnumeric():
        return False
    try:
        # Tenta passar o número de telefone usando a biblioteca phonenumbers.
        numero_fone_parseado = phonenumbers.parse(phone_number, "BR")
        # Valida se o número de telefone é válido.
        if phonenumbers.is_valid_number(numero_fone_parseado):
            return True
        else:
            return False
    except phonenumbers.NumberParseException:
        # Se o número de telefone não puder ser passar, ele é inválido.
        return False

# validando cep
def is_valid_cep(cep):
    # Removendo espaços e hifens
    cep = cep.replace(" ", "").replace("-", "")

    # Valida o formato do CEP
    if not re.match(r"^\d{5}-\d{3}$", cep):
        return False

    # Consulta a API dos Correios
    response = requests.get(f"https://viacep.com.br/ws/cep/{cep}/json/")
    if response.status_code == 200:
        data = response.json()
        if "erro" in data:
            return False
        else:
            return True
    else:
        return False 

# Validando cnpj
def valida_cnpj(_cnpj):
 
    # Remove caracteres especiais
    cnpj = apenas_numeros(_cnpj)

    # Valida o tamanho do CNPJ
    if len(cnpj) != 14:
        return False

    # Separa os dígitos do CNPJ
    digitos = list(cnpj)

    # Calcula o primeiro dígito verificador
    soma1 = 0
    for indice, digito in enumerate(digitos[:12]):
        soma1 += int(digito) * (13 - indice)
    soma1 = soma1 % 11
    if soma1 == 0:
        digitos.append('0')
    else:
        digitos.append(str(11 - soma1))

    # Calcula o segundo dígito verificador
    soma2 = 0
    for indice, digito in enumerate(digitos):
        soma2 += int(digito) * (14 - indice)
    soma2 = soma2 % 11
    if soma2 == 0:
        digitos.append('0')
    else:
        digitos.append(str(11 - soma2))

    # Compara os dígitos verificadores calculados com os dígitos informados
    if digitos[12] != digitos[13] or digitos[13] != digitos[14]:
        return False

    return Tru


######################################### VALIDANDO DADOS DE USUÁRIO #########################################

def user_valid_data(request, username, email, password, confirm_password):
    # verifica espaços em branco
    if (len(username.strip()) == 0) or (len(email.strip()) == 0) or (len(password.strip()) == 0) or (len(confirm_password.strip()) == 0):
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return False
    
    # Verifica se usuários já existem
    verifyName = User.objects.filter(username=username).first()  
    verifyEmail = User.objects.filter(email=email).first()

    if len(username) < 3:
        messages.add_message(request, constants.ERROR, "O nome do usuário é preciso no mínimo 3 caracteres")
        return False
    elif verifyName is not None:
        messages.add_message(request, constants.ERROR, "Este usuário já existe")
        return False
    elif verifyEmail is not None:
        messages.add_message(request, constants.ERROR, "Este email já está sendo usado por outro usuário")
        return False    
    
    # Verificador de senha
    if not password_is_valid(request, password, confirm_password):
            return False
    
    print("Sua empresa passou por todas as validações!")
    return True
######################################### VALIDANDO OS DADOS DA EMPRESA #######################################

def company_valid_data(request, name_company, cnpj, phone, address, cep, city, state):
    # if (len(name_company.strip()) == 0) or (len(cnpj.strip()) == 0) or (len(phone.strip()) == 0) or (len(state.strip()) == 0) or (len(address.strip()) == 0 or (len(city.strip()) == 0)):
    #         messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
    #         return False
   
    # Verifica se o cnpj é válido   
    # if not valida_cnpj(cnpj):
    #     messages.add_message(request, constants.ERROR,"Digite um cnpj válido.")
    #     return False
        
    # Verifica se o número de telefone é válido    
    if not valid_phone_number(phone):
        messages.add_message(request, constants.ERROR, "Digite um número de telefone válido")
        return False  
       
 
    
    # Verifica se o CEP é válido
    
    # if not is_valid_cep(cep):
    #     messages.add_message(request, constants.ERROR, "Digite um CEP válido")
    #     return False
    
    # verifica se já existe um usuário com algum desses dados
    verifyName = Company.objects.filter(name_company=name_company).first()
    verifyCnpj = Company.objects.filter(cnpj=cnpj).first()
  

    # if len(name_company) < 3:
    #     messages.add_message(request, constants.ERROR, "O nome do usuário é preciso no mínimo 3 caracteres")
    #     return False
    if verifyName is not None:
        messages.add_message(request, constants.ERROR, "Este usuário já existe")
        return False
    elif verifyCnpj is not None:
        messages.add_message(request, constants.ERROR, "Este cnpj já está cadastrado")
        return False
     

    return True 
    
  
# ATIVAÇÃO DE CONTA   
def email_html(path_template: str, subject: str, to: list, **kwargs) -> dict:
    
    html_content = render_to_string(path_template, kwargs)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, to)

    email.attach_alternative(html_content, "text/html")
    email.send()
    return {'status': 1}