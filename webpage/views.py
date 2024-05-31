from django.http import HttpResponse
from django.template import loader

from listapresente.models import Produto


# Create your views here.
def home(request):
    template = loader.get_template("index.html")
    context = {
        "noivo": "Erivaldo",
        "noiva": "Evelyn",
        "data_casamento": "07 Dezembro",
    }
    return HttpResponse(template.render(context, request))


def lista_de_presentes(request):
    template = loader.get_template("lista-de-presentes.html")
    produtos = Produto.objects.all()
    context = {
        "produtos": produtos,
    }
    return HttpResponse(template.render(context, request))
