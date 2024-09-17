from django.forms import ModelForm, TextInput, EmailInput

from listapresente.models import Comprador


class CompradorForm(ModelForm):
    class Meta:
        model = Comprador
        fields = ('nome','sobrenome','email','telefone')
        labels = {
            'nome': 'Nome',
            'sobrenome': 'Sobrenome',
            'email': 'Email',
            'telefone': 'Telefone',
        }
        widgets = {
        'nome': TextInput(attrs={'class': "form-control"}),
        'sobrenome': TextInput(attrs={'class': "form-control"}),
        'email': EmailInput(attrs={'class': "form-control"}),
        'telefone': TextInput(attrs={'class': "form-control"}),

        }