from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from listapresente.forms import CompradorForm
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
    comprador_form = CompradorForm(request.POST)
    template = loader.get_template("presente.html")
    produto = Produto.objects.get(id=id_presente)
    context = {
        "comprador_form": comprador_form,
        "produto": produto,
    }
    return HttpResponse(template.render(context, request))


def pagar(request, id_presente):
    if request.method == 'POST':
        comprador_form = CompradorForm(request.POST)
        if comprador_form.is_valid():
            print("formulario valido")
            produto = Produto.objects.get(id=id_presente)
            url = obter_link_produto(produto.nome, produto.descricao, request.build_absolute_uri(produto.imagem.url),
                                     produto.preco, request.get_host())
            return HttpResponseRedirect(url)
