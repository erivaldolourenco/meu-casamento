from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from listapresente.models import Produto
from pagamentos.mercadopago.preferencia import obter_link_produto


# Create your views here.
def lista_de_presentes(request):
    template = loader.get_template("lista-de-presentes.html")
    produtos = Produto.objects.all()
    context = {
        "produtos": produtos,
    }
    return HttpResponse(template.render(context, request))


def presente(request, id_presente):
    template = loader.get_template("presente.html")
    produto = Produto.objects.get(id=id_presente)
    context = {
        "produto": produto,
    }
    return HttpResponse(template.render(context, request))


def pagar(request, id_presente):
    produto = Produto.objects.get(id=id_presente)
    url = obter_link_produto(produto.nome, produto.descricao, request.build_absolute_uri(produto.imagem.url),
                             produto.preco, request.get_host())
    return HttpResponseRedirect(url)
