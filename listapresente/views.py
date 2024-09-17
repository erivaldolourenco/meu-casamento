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
            codigo = re.search(r'\((\d{2})\)', comprador.telefone).group(1)
            telefone = re.search(r'\)\s*(\d{5}-\d{4})', comprador.telefone).group(1)
            produto = Produto.objects.get(id=id_presente)
            url = obter_link_produto(comprador.nome, comprador.sobrenome, comprador.email, telefone, codigo,
                                     produto.id, produto.nome, produto.descricao, request.build_absolute_uri(produto.imagem.url),
                                     produto.preco, request.get_host())
            return HttpResponseRedirect(url)


def pagamento_sucesso(request):
    payment_id = request.GET.get('payment_id')
    status = request.GET.get('status')
    preference_id = request.GET.get('preference_id')
    preference = obter_preferencia(preference_id)
    produto = preference['items'][0]
    comprador = preference['payer']

    convidado_presente, criado = ConvidadoPresente.objects.get_or_create(
        id_pagamento=payment_id,
        defaults={
            'nome_convidado': comprador['name'],
            'id_preferencia': preference_id,
            'sobrenome_convidado': comprador['surname'],
            'email': comprador['email'],
            'produto_nome': produto['title'],
            'produto_descricao': produto['description'],
            'status': status
        }
    )

    if not criado:
        convidado_presente.nome_convidado = comprador['name']
        convidado_presente.sobrenome_convidado = comprador['surname']
        convidado_presente.email = comprador['email']
        convidado_presente.produto_nome = produto['title']
        convidado_presente.produto_descricao = produto['description']
        convidado_presente.status = status
        convidado_presente.id_preferencia = preference_id
        convidado_presente.save()

    if not status == 'pending':
        template = loader.get_template("pagamento_sucesso.html")
    else:
        template = loader.get_template("pagamento_pendente.html")
    context = {
        "nome": comprador['name'],
        "sobrenome": comprador['surname']
    }
    return HttpResponse(template.render(context, request))


def pagamento_erro(request):
    template = loader.get_template("pagamento_erro.html")
    context = {}
    return HttpResponse(template.render(context, request))


@csrf_exempt
def notificacao_mercadopago(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            id_pagamento = data.get('data', {}).get('id')

            if not id_pagamento:
                return HttpResponse("ID do pagamento não encontrado", status=400)

            pagamento_response = obter_pagamento(id_pagamento)
            if not pagamento_response.get('response'):
                return HttpResponse("Pagamento não encontrado", status=404)

            pagamento = pagamento_response.get('response')

            if pagamento.get('status') == 'approved':
                pagador = pagamento.get('payer', {})
                detalhes = pagamento.get('transaction_details', {})
                produto = Produto.objects.get(id=pagamento['additional_info']['items'][0]['id'])
                if produto.quantidade > 0:
                    produto.quantidade -= 1
                    produto.save()
                else:
                    raise ValueError('Estoque insuficiente para o produto.')

                data_criacao = datetime.strptime(pagamento.get('date_created', '').replace('Z', ''),
                                                 "%Y-%m-%dT%H:%M:%S.%f%z")
                data_compra = data_criacao.date()
                telefone = pagamento['additional_info']['payer']['phone']
                cod_telefone = str(telefone['area_code']) + str(telefone['number']).replace("-", "")

                convidado_presente, criado = ConvidadoPresente.objects.get_or_create(
                    id_pagamento=id_pagamento,
                    defaults={
                        'nome_convidado': pagamento['additional_info']['payer']['first_name'],
                        'sobrenome_convidado': pagamento['additional_info']['payer']['last_name'],
                        'email': pagamento['additional_info']['payer']['last_name'],
                        'produto_nome': produto.nome,
                        'produto_descricao': produto.descricao,
                        'status': pagamento['status'],
                        'valor_recebido': detalhes.get('net_received_amount', 0),
                        'data_compra': data_compra,
                        'telefone': cod_telefone
                    }
                )

                if not criado:
                    convidado_presente.valor_recebido = detalhes.get('net_received_amount', 0)
                    convidado_presente.data_compra = data_compra
                    convidado_presente.status = pagamento.get('status')
                    convidado_presente.telefone = cod_telefone
                    convidado_presente.save()

                mensagem = (f"🤑💰 <b>{convidado_presente.nome_convidado} {convidado_presente.sobrenome_convidado}</b>"
                            f" lhe presenteou com um <u>{produto.nome}</u>, no valor de:<b> R$ {detalhes.get('net_received_amount', '0')}</b>💰🤑")
                enviar_telegram(mensagem)

                return HttpResponse(status=200)
            else:
                print(f"Pagamento não aprovado, status: {pagamento.get('status')}. ID do pagamento: {id_pagamento}")
                return HttpResponse(status=400)

        except json.JSONDecodeError:
            return HttpResponse("Erro ao processar JSON", status=400)

        except Exception as e:
            print(str(e))
            return HttpResponse("Erro interno do servidor", status=500)
    return HttpResponse("Método não permitido", status=405)
