import mercadopago

from config.config_util import ConfigUtil

ConfigUtil.load_env()
sdk = mercadopago.SDK(ConfigUtil.get_token_mercadopago())


def obter_link_produto(nome, descricao, imagem_url, valor, dominio):
    request_options = mercadopago.config.RequestOptions()
    request_options.custom_headers = {
        'x-idempotency-key': '<SOME_UNIQUE_VALUE>'
    }

    payment_data = {
        "items": [
            {
                "id": "1234",
                "title": nome,
                "description": descricao,
                "picture_url": imagem_url,
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": float(valor),
            }
        ],
        "back_urls": {
            "success": dominio + "/sucesso",
            "failure": dominio + "/falha",
            "pending": dominio + "/falha",
        },
    }
    result = sdk.preference().create(payment_data, request_options)
    return result["response"]["init_point"]
