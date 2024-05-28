from django.http import HttpResponse
from django.template import loader


# Create your views here.
def home(request):
    template = loader.get_template("index.html")
    context = {
        "noivo": "Erivaldo",
        "noiva": "Evelyn",
        "data_casamento": "07 Dezembro",
    }
    return HttpResponse(template.render(context, request))