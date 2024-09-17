import mercadopago

from config.config_util import ConfigUtil

ConfigUtil.load_env()
sdk = mercadopago.SDK(ConfigUtil.get_token_mercadopago())


def obter_link_produto(nome_comprador, sobrenome_comprador, email_comprador, telefone_comprador, codigo_telefone,
                       id_produto, nome_produto, descricao_produto, imagem_url, valor_produto, dominio):

    payment_data = {
        "items": [
            {
                "id": id_produto,
                "title": nome_produto,
                "description": descricao_produto,
                "picture_url": imagem_url,
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": float(valor_produto),
            }
        ],
        "payer": {
            "name": nome_comprador,
            "surname": sobrenome_comprador,
            "email": email_comprador,
            "phone": {
                "area_code": codigo_telefone,
                "number": telefone_comprador,
            },
        },
        "back_urls": {
            "success": dominio + "/lista-de-presente/pagamento-sucesso",
            "failure": dominio + "/lista-de-presente/pagamento-erro",
            "pending": dominio + "/lista-de-presente/pagamento-sucesso",
        },
        "auto_return": "all",
        "statement_descriptor": "Presente de Casamento"
    }
    preference_response = sdk.preference().create(payment_data)
    return preference_response["response"]["init_point"]


def obter_preferencia(id):
    preference_response = sdk.preference().get(id)
    return preference_response["response"]

def obter_pagamento(id):
    return sdk.payment().get(id)