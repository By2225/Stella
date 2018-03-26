#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import random
import requests
import os
from flask import Flask, request, render_template
from pymessenger.bot import Bot

app = Flask(__name__)

ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
STELLAR_API_URL = 'https://stellarapi.herokuapp.com/'
bot = Bot(ACCESS_TOKEN)

@app.route('/', methods=['GET', 'POST'])
def receive_message():
    """Processes Facebook postback messages"""

    if request.method == 'GET':
        # Confirms that messages are sent from Facebook and subscribes webhook to bot
        token_sent = request.args.get('hub.verify_token')
        if token_sent == VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        return 'Invalid verification token'

    req_json = request.get_json()
    for event in req_json['entry']:
        messaging = event['messaging']
        for message in messaging:
            # Forward all Get Started postback messages to user
            if 'postback' in message:
                postback = message['postback']
                title = postback['title']
                if title == 'Get Started':
                    send_message(message['sender']['id'],
                        message['postback']['payload'])
    return 'Message Processed'

def send_message(recipient_id, response):
    """Sends the user a text message
    Args:
        recipient_id: Facebook id of message recipient
        response: Text message to send user
    """
    bot.send_text_message(recipient_id, response)
    return 'success'

@app.route("/balance_form", methods=['GET', 'POST'])
def get_balance_form():
    """Renders the check balance form"""
    return render_template('balance/index.html')

@app.route("/get_balance", methods=['POST'])
def get_balance():
    """Fetches the balance of a Stellar account"""
    result = request.form
    accountId = result['accountId']
    resp = requests.post(STELLAR_API_URL + 'getBalance',
        {'accountId': accountId})

    data = json.loads(resp.text)
    if resp.status_code == 200:
        balance = data['balance']
        account = data['account']
        return render_template('balance/balance.html',
            balance=balance, account=account)
    else:
        return render_template('error.html', error=resp.status_code)

@app.route('/key_pair_form', methods=['GET', 'POST'])
def key_pair_form():
    """Renders the create key pair webpage"""
    return render_template('create-key-pair/index.html')

@app.route('/create_key_pair', methods=['GET', 'POST'])
def create_key_pair():
    """Creates an account key pair (account id, secret seed)"""
    resp = requests.post(STELLAR_API_URL + 'createKeyPair')
    if resp.status_code == 200:
        data = json.loads(resp.text)
        secretSeed = data['secretSeed']
        accountId = data['accountId']
        return render_template('create-key-pair/keypair.html',
            accountId=accountId, secretSeed=secretSeed)
    else:
        return render_template('error.html', error=resp.status_code)

@app.route('/registration_form', methods=['GET', 'POST'])
def get_registration_form():
    """Renders the account registration form"""
    return render_template('register-testnet/index.html')

@app.route("/register_testnet_acct", methods=['POST'])
def register_testnet():
    """Registers and funds an account on the Stellar testnet"""
    result = request.form
    accountId = result['accountId']
    resp = requests.post(STELLAR_API_URL + 'registerTestNetAccount',
                         {'accountId': accountId})
    if resp.status_code == 200:
        return render_template('register-testnet/registration.html')
    else:
        return render_template('error.html', error=resp.status_code)

@app.route('/payment_form', methods=['GET', 'POST'])
def get_payment_form():
    """Renders the form for submitting a payment"""
    return render_template('send/index.html')

@app.route('/send_lumens', methods=['POST'])
def send_lumens():
    """Sends lumens to destination account"""
    result = request.form
    dest_acct_id = result['destAcctId']
    secret_seed = result['secretSeed']
    amount = result['amount']
    resp = requests.post(STELLAR_API_URL + 'send',
                         {'secretSeed': secret_seed,'destAcctId': dest_acct_id,
                            'amount': amount})
    if resp.status_code == 200:
        return render_template('send/sent.html',
            destAcctId=dest_acct_id, secretSeed=secret_seed, amount=amount)
    else:
        return render_template('error.html', error=resp.status_code)

if __name__ == '__main__':
    app.run()
