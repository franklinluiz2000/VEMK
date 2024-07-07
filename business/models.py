from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe


class Company(models.Model):
    choice_plan =((1,"Gratis"),(2,"Básico"),(3, "Premium")) 
    # user = models.(User, on_delete=models.CASCADE)       
    name_company = models.CharField(max_length=100, null=False, blank=False)
    cnpj = models.CharField(max_length=20)
    phone = models.CharField(max_length=19)
    address = models.CharField(blank=True, max_length=100)
    cep = models.CharField(blank=True, max_length=11)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=20)            
    chosen_plan = models.IntegerField(choices=choice_plan, default=1)
    linked_user = models.ForeignKey(User, related_name='linked_user', on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    active = models.BooleanField(default=True)
  

    def __str__(self):
        return self.name_company
    



        
class Category(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category





class Product(models.Model):
    product_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_img')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField()
    description = models.TextField()
    active = models.BooleanField(default=True)
    linked_company = models.ForeignKey(Company, related_name='linked_company', on_delete=models.CASCADE)

    @mark_safe
    def icone(self):
        return f'<img width="30px" src="/media/{self.img}">'


    def __str__(self):
        return self.product_name


