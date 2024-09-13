from django.forms import ModelForm, TextInput

from listapresente.models import Comprador


class CompradorForm(ModelForm):
    class Meta:
        model = Comprador
        fields = ('nome','sobrenome','cpf','email','telefone')
        labels = {
            'nome': 'Nome',
            'sobrenome': 'Sobrenome',
            'cpf': 'CPF',
            'email': 'Email',
            'telefone': 'Telefone',
        }
        widgets = {
        'nome': TextInput(attrs={'class': "form-control"}),
        'sobrenome': TextInput(attrs={'class': "form-control"}),
        'cpf': TextInput(attrs={'class': "form-control"}),
        'email': TextInput(attrs={'class': "form-control"}),
        'telefone': TextInput(attrs={'class': "form-control"}),

        }