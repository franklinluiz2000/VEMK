from django.db import models
from django.contrib.auth.models import User
from .utils import validate_email_with_domain

class Company(models.Model):
    choice_plan =((1,"Gratis"),(2,"Básico"),(3, "Premium"))
    name = models.CharField(max_length=100, null=False, blank=False)
    cnpj = models.CharField(max_length=20, null=False, blank=False)
    email = models.EmailField(max_length=254, validators=[validate_email_with_domain])
    address = models.CharField(blank=True, max_length=100)
    cep = models.CharField(blank=True, max_length=11)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=19)
    image = models.ImageField(null=True, blank=True)    
    chosen_plan = models.IntegerField(choices=choice_plan, default=1)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name



class Activation(models.Model):
    token = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
