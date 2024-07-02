from django.contrib import messages
from django.contrib.messages import constants
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import re
import phonenumbers
import requests
from django.core.validators import EmailValidator
from django.core.validators import validate_email
import dns.resolver




def password_is_valid(request, password, confirm_password):
    if len(password) < 6:
        messages.add_message(request, constants.ERROR, 'Sua senha deve conter 6 ou mais caractertes')
        return False
    print(password)
    print(confirm_password)
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


def email_html(path_template: str, subject: str, to: list, **kwargs) -> dict:
    
    html_content = render_to_string(path_template, kwargs)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, to)

    email.attach_alternative(html_content, "text/html")
    email.send()
    return {'status': 1}



def valid_phone_number(phone_number):  

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
    



def validate_cnpj(cnpj):
    cnpj_regex = re.compile(r"^\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}$")
    # Remove caracteres especiais
    cnpj = cnpj.replace(".", "").replace("/", "").replace("-", "")

    # Valida o formato geral
    if not cnpj_regex.match(cnpj):
        return False

    # Cálculo dos dígitos verificadores
    soma1 = 0
    soma2 = 0
    for i, digit in enumerate(cnpj):
        digit = int(digit)
        soma1 += (i + 1) * digit
        if i < 13:
            soma2 += digit

    soma1 = 11 - (soma1 % 11) if soma1 % 11 != 0 else 0
    soma2 = 11 - (soma2 % 11) if soma2 % 11 != 0 else 0

    # Verifica se os dígitos verificadores conferem
    if cnpj[-2:] != f"{soma1}{soma2}":
        return False

    return True


# Validando o email
def validate_email_with_domain(email_address):    
    try:
        # verifica o formato (sintaxe)
        validate_email(email_address)
    except:
        return False

    # Ssepara somente o dominio
    domain = email_address.split('@')[-1]

    # verifica se o dominio existe
    try:
        mx_records = dns.resolver.query(domain, 'MX')
    except dns.resolver.NXDOMAIN:
        return False

    # retorna se o dominio não é valido
    if not mx_records:
        return False

    return True