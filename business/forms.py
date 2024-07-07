from django import forms
from .models import Product, Company



class CompanyForm(forms.ModelForm):

    name_company = forms.CharField(label="Nome da empresa", widget=forms.TextInput({'class': 'form-control'}), required=True)
    cnpj = forms.CharField(label="Número do CNPJ", widget=forms.NumberInput(attrs={'class': 'form-control'}), max_length=14, required=True)
    phone = forms.CharField(label="Número para contato", widget=forms.NumberInput(attrs={'class': 'form-control'}), max_length=11, required=True)
    address = forms.CharField(label="Endereço", widget=forms.TextInput(attrs={'class': 'form-control'}),max_length=100, required=True)
    cep = forms.CharField(label="CEP", widget=forms.NumberInput(attrs={'class': 'form-control'}), max_length=8, required=True)
    city = forms.CharField(label="Cidade", widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    state = forms.CharField(label="Estado", widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    chosen_plan = forms.Select({'class': "form-control"})
    image = forms.ImageField(label="foto do produto", widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)
    
    
    
    class Meta:
        model = Company
        fields = ['name_company', 'cnpj', 'phone', 'address', 'cep', 'city', 'state', 'chosen_plan', 'image']

       
class ProductForm(forms.ModelForm):
   
    product_name = forms.CharField(label="Nome do produto", widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    image = forms.ImageField(label="foto do produto", widget=forms.FileInput(attrs={'class': 'form-control'}))
    category = forms.Select({'class': "form-control"})
    price = forms.CharField(label="Valor do produto",widget=forms.NumberInput(attrs={'class': 'form-control'}), max_length=5, required=True)
    description = forms.CharField(label="Descrição do produto", widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Product
        fields = ['product_name', 'price', 'description', 'category', 'image']
