from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from alertas.telegram.telegram import enviar_telegram
from convidados.forms import ConvidadoForm, AcompanhanteFormSet
from convidados.models import Convidado


# Create your views here.
def presenca(request):
    if request.method == 'POST':
        convidado = Convidado()
        acompanhantes = []
        form_convidado = ConvidadoForm(request.POST)
        formset_acompanhantes = AcompanhanteFormSet(request.POST)
        template = loader.get_template("presenca.html")
        try:
            if form_convidado.is_valid() and formset_acompanhantes.is_valid():
                convidado = form_convidado.save()
                formset_acompanhantes.instance = convidado
                formset_acompanhantes.save()
                acompanhantes = formset_acompanhantes.cleaned_data
                enviar_telegram(convidado.nome + " confirmou a presença!")
        except Convidado.DoesNotExist:
            convidado = None
            acompanhantes = None
        context = {
            "convidado": convidado,
            "acompanhantes": acompanhantes,

        }
        return HttpResponse(template.render(context, request))

def lista(request):
    convidados = Convidado.objects.all()

    template = loader.get_template("lista_convidados.html")
    context = {
        "convidados": convidados,
        "teste": dir(convidados[0]),
    }
    return HttpResponse(template.render(context, request))

# def carregar(request):
#     # Lista de convidados e acompanhantes
#     nomes = [
#         "Elisbene", "Camila", "Carla", "Esposo Carla", "Junior", "Esposa Junior",
#         "Erli", "Marco", "Esposa Marco", "Ruan", "Esposa Ruan", "Ludimila",
#         "Esposo Ludimila", "Leonildo", "Esposa Leonildo", "Andreazo", "Alisson",
#         "Raveli", "Esposa Raveli", "Cicero", "Esposa Cicero", "Juarez", "Esposa Juarez",
#         "Alexandre", "Esposa Alexandre", "Manoel", "Adriana", "Adriele", "Antonio",
#         "Esposa Antonio", "Maria Clara", "Edilson", "Paula", "Patricia", "Fabio",
#         "Luana", "Erikles", "Lucenildo", "Lucicleide", "Milena", "Joana", "Reumer",
#         "Esposa Reumer", "Lucimar", "Willames", "Esposa", "Isaias", "Samuel",
#         "Renata", "Elton", "Esposa Elton", "Rafael", "Esposa Rafael", "Jonathan Batman",
#         "Esposa Batman", "Jonathan Gordinho", "Esposa Gordinho", "Fran", "Esposo Fran",
#         "Raul", "Esposa Raul", "Rafha", "Italo", "Beto", "Esposa Beto", "Pr Walter",
#         "Esposa Walter", "Maria Clara – filha Alisson", "Matheus - filho Alisson",
#         "Maria voinha", "Sânia", "Jose Roberto", "Samuel", "Saulo", "Elifio", "Esposa",
#         "Tio Sandro", "Tia Andrea", "Milca", "Gustavo", "Miguel", "Daniel", "Kris",
#         "Eduardo", "Kaline", "Diego", "Lana", "Thamison", "Isa", "Jhon", "Camila",
#         "Marcos", "Bea", "Henrique", "Caique", "Luysa", "Matheus", "Aninha", "Nicole",
#         "Joao", "Reinaldo", "Esposa Reinaldo", "Filho Reinaldo", "Pr Roseane", "Ana",
#         "namorado", "Rodolfo", "Tati"
#     ]
#     for nome in nomes:
#         convidado = Convidado.objects.create(nome=nome)
#         convidado.save()
#
#     return HttpResponse("CONVIDADOS CARREGADOS")