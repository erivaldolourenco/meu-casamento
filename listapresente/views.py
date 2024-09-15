import json
import re
from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from alertas.telegram.telegram import enviar_telegram
from convidados.models import ConvidadoPresente
from listapresente.forms import CompradorForm
from listapresente.models import Produto
from pagamentos.mercadopago.preferencia import obter_link_produto, obter_preferencia, obter_pagamento

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
            url = obter_link_produto(comprador.nome, comprador.sobrenome, comprador.email, telefone, codigo,
                                     cpf_comprador, produto.nome,
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
    site_id = request.GET.get('site_id')
    processing_mode = request.GET.get('processing_mode')
    merchant_account_id = request.GET.get('merchant_account_id')
    preference_id = request.GET.get('preference_id')
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
    context = {}
    return HttpResponse(template.render(context, request))

def pagamento_pendente(request):
    template = loader.get_template("pagamento_pendente.html")
    context = {}
    return HttpResponse(template.render(context, request))


@csrf_exempt
def notificacao_mercadopago(request):
    if request.method == 'POST':
        try:
            # Converte o corpo da requisição em JSON
            data = json.loads(request.body)

            # Extrai os dados da notificação
            pagamento_id = data.get('id')
            live_mode = data.get('live_mode')
            tipo = data.get('type')
            data_criacao_str = data.get('date_created')
            usuario_id = data.get('user_id')
            versao_api = data.get('api_version')
            acao = data.get('action')
            id_pagamento = data.get('data', {}).get('id')

            if not id_pagamento:
                # Se não houver id do pagamento, retorna erro
                return HttpResponse("ID do pagamento não encontrado", status=400)

            # Obtém detalhes do pagamento usando a função 'obter_pagamento'
            pagamento = obter_pagamento(id_pagamento)
            if not pagamento:
                # Se não conseguir obter o pagamento, retorna erro
                return HttpResponse("Pagamento não encontrado", status=404)

            if pagamento.get('status') == 'approved':
                pagador = pagamento.get('payer', {})
                detalhes = pagamento.get('transaction_details', {})
                data_criacao = datetime.strptime(pagamento.get('date_created', ''), "%Y-%m-%dT%H:%M:%S.%fZ")
                data_compra = data_criacao.date()

                convidado_presente = ConvidadoPresente(
                    cpf=pagador.get('identification', {}).get('number', 'Não informado'),
                    email=pagador.get('email', 'Não informado'),
                    preco=detalhes.get('net_received_amount', 0),
                    presente=pagamento.get('description', 'Descrição não disponível'),
                    data_compra=data_compra,
                )
                convidado_presente.save()

                # Envia mensagem para o Telegram
                mensagem = f"Recebemos um presente de: {pagador.get('email', 'Desconhecido')} no valor de: {detalhes.get('net_received_amount', '0')}"
                enviar_telegram(mensagem)

                return HttpResponse(status=200)
            else:
                # Se o pagamento não for aprovado
                enviar_telegram(f"Pagamento não aprovado. ID do pagamento: {id_pagamento}")
                return HttpResponse(status=400)

        except json.JSONDecodeError:
            # Se o JSON estiver mal formatado
            return HttpResponse("Erro ao processar JSON", status=400)

        except Exception as e:
            # Captura qualquer outra exceção e loga o erro
            enviar_telegram(f"Erro ao processar notificação: {str(e)}")
            return HttpResponse("Erro interno do servidor", status=500)

    # Se o método HTTP não for POST
    return HttpResponse("Método não permitido", status=405)
