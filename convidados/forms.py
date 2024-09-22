from django import forms
from django.forms import inlineformset_factory, TextInput
from .models import Convidado, Acompanhante


# Formulário de Convidado
class ConvidadoForm(forms.ModelForm):
    tem_acompanhante = forms.BooleanField(required=False, label="Tem acompanhante?")
    class Meta:
        model = Convidado
        fields = ['nome']

        labels = {
            'nome': 'Nome completo.',

        }
        widgets = {
            'nome': TextInput(attrs={'class': "form-control"}),
        }


# Formulário inline para Acompanhantes, relacionado com o Convidado
AcompanhanteFormSet = inlineformset_factory(
    Convidado, Acompanhante,
    form=forms.ModelForm,
    fields=['nome'],
    labels = {'nome': 'Nome completo.' },
    widgets={'nome': TextInput(attrs={'class': "form-control"})},
    extra=1, can_delete=False
)
