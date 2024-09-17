import mercadopago
from mercadopago.config import RequestOptions

request_options = RequestOptions(access_token='TEST-4398345889891464-091700-8613ae160df3f80b73b46f43616b3237-495427135')
# ...
sdk= mercadopago.SDK("TEST-4398345889891464-091700-8613ae160df3f80b73b46f43616b3237-495427135")

payment_data = {
    "items": [
        {
            "id": "1",
            "title": "Produto 1",
            "quantity": 1,
            "currency_id": "BRL",
            "unit_price": 100.0
        }
    ],
    "back_urls": {
        "success": "http://localhost:5000/compra_certa",
        "failure": "http://localhost:5000/compra_errada",
        "pending": "http://localhost:5000/compra_errada"
    },
    "auto_return": "all",
}

result = sdk.payment().create(payment_data, request_options)
payment = result["response"]