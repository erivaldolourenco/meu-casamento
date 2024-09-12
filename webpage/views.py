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

def manutencao(request):
    template = loader.get_template("manutencao.html")
    context = {
    }
    return HttpResponse(template.render(context, request))
