from flask import Flask, render_template, redirect, request
from uuid import uuid4
from phonepe.sdk.pg.payments.v2.standard_checkout_client import StandardCheckoutClient
from phonepe.sdk.pg.payments.v2.models.request.standard_checkout_pay_request import StandardCheckoutPayRequest
from phonepe.sdk.pg.env import Env
import os

app = Flask(__name__)

client = StandardCheckoutClient.get_instance(
    client_id=os.getenv("PHONEPE_CLIENT_ID"),
    client_secret=os.getenv("PHONEPE_CLIENT_SECRET"),
    client_version=int(os.getenv("PHONEPE_CLIENT_VERSION", "1")),
    env=Env.SANDBOX
)

REDIRECT_URL = os.getenv("REDIRECT_URL", "https://shareautotaxfiling.onrender.com/success")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/file-itr')
def file_itr():
    return render_template('file_itr.html')

@app.route('/pay/<int:amount>', methods=['POST'])
def pay(amount):
    order_id = str(uuid4())
    payment_request = StandardCheckoutPayRequest.build_request(
        merchant_order_id=order_id,
        amount=amount * 100,
        redirect_url=REDIRECT_URL
    )
    response = client.pay(payment_request)
    return redirect(response.redirect_url)

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)