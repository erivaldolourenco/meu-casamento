import re

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from listapresente.forms import CompradorForm
from listapresente.models import Produto
from pagamentos.mercadopago.preferencia import obter_link_produto, obter_preferencia


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


def pagamento(request, id_presente):
    if request.method == 'POST':
        comprador_form = CompradorForm(request.POST)
        if comprador_form.is_valid():
            comprador = comprador_form.save(commit=False)
            cpf_comprador = comprador.cpf.replace('.', '').replace('-', '')
            codigo = re.search(r'\((\d{2})\)', comprador.telefone).group(1)
            telefone = re.search(r'\)\s*(\d{5}-\d{4})', comprador.telefone).group(1)
            produto = Produto.objects.get(id=id_presente)
            url = obter_link_produto(comprador.nome, comprador.sobrenome, comprador.email,telefone, codigo,cpf_comprador, produto.nome,
                                     produto.descricao, request.build_absolute_uri(produto.imagem.url),
                                     produto.preco, request.get_host())
            return HttpResponseRedirect(url)

def pagamento_sucesso(request):
    collection_id = request.GET.get('collection_id')
    collection_status = request.GET.get('collection_status')
    payment_id = request.GET.get('payment_id')
    status = request.GET.get('status')
    external_reference = request.GET.get('external_reference')
    payment_type = request.GET.get('payment_type')
    merchant_order_id = request.GET.get('merchant_order_id')
    preference_id = request.GET.get('preference_id')
    site_id = request.GET.get('site_id')
    processing_mode = request.GET.get('processing_mode')
    merchant_account_id = request.GET.get('merchant_account_id')

    preference = obter_preferencia(preference_id)
    comprador = preference['payer']

    template = loader.get_template("pagamento_sucesso.html")
    context = {
        "nome": comprador['name'],
        "sobrenome": comprador['surname']
    }
    return HttpResponse(template.render(context, request))

def pagamento_erro(request):
    template = loader.get_template("pagamento_erro.html")
    context = {
        "nome": "Um Nome aqui",
    }
    return HttpResponse(template.render(context, request))