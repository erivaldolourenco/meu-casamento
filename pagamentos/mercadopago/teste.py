
import mercadopago

if __name__ == '__main__':
    sdk = mercadopago.SDK("")


    search_request = sdk.payment().get(87925477996)

    print(search_request)