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
    payment_id = request.GET.get('payment_id')
    status = request.GET.get('status')
    preference_id = request.GET.get('preference_id')
    preference = obter_preferencia(preference_id)
    produto = preference['items'][0]
    comprador = preference['payer']

    if not ConvidadoPresente.objects.filter(id_pagamento=payment_id).exists():
        convidado_presente = ConvidadoPresente(
            nome_convidado=comprador['name'],
            sobrenome_convidado= comprador['surname'],
            id_pagamento=payment_id,
            email=comprador['email'],
            produto_nome=produto['title'],
            produto_descricao=produto['description'],
            status=status
        )
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
                return HttpResponse("ID do pagamento não encontrado", status=400)

            pagamento_response = obter_pagamento(id_pagamento)
            if not pagamento_response.get('response'):
                return HttpResponse("Pagamento não encontrado", status=404)

            pagamento = pagamento_response.get('response')


            if pagamento.get('status') == 'approved':
                pagador = pagamento.get('payer', {})
                detalhes = pagamento.get('transaction_details', {})
                data_criacao = datetime.strptime(pagamento.get('date_created', '').replace('Z', ''), "%Y-%m-%dT%H:%M:%S.%f%z")
                data_compra = data_criacao.date()

                if ConvidadoPresente.objects.filter(id_pagamento=id_pagamento).exists():
                    convidado_presente = ConvidadoPresente.objects.get(id_pagamento=id_pagamento)
                    convidado_presente.valor_recebido = detalhes.get('net_received_amount', 0)
                    convidado_presente.data_compra = data_compra
                    convidado_presente.status = pagamento.get('status')
                    convidado_presente.save()
                else:
                    convidado_presente = ConvidadoPresente(
                        nome_convidado='Foi criado notificacao',
                        id_pagamento=id_pagamento,
                        valor_recebido=detalhes.get('net_received_amount', 0),
                        data_compra=data_compra,
                        status=pagamento.get('status')
                    )
                    convidado_presente.save()

                mensagem = f"Recebemos um presente de: {pagador.get('email', 'Desconhecido')} no valor de: {detalhes.get('net_received_amount', '0')}"
                enviar_telegram(mensagem)

                return HttpResponse(status=200)
            else:
                print(f"Pagamento não aprovado, status: {pagamento.get('status')}. ID do pagamento: {id_pagamento}")
                return HttpResponse(status=400)

        except json.JSONDecodeError:
            return HttpResponse("Erro ao processar JSON", status=400)

        except Exception as e:
            print(str(e))
            enviar_telegram(f"Erro ao processar notificação: {str(e)}")
            return HttpResponse("Erro interno do servidor", status=500)

    # Se o método HTTP não for POST
    return HttpResponse("Método não permitido", status=405)
