import random
import requests
import os
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)

ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
STELLAR_API_URL = "https://stellarapi.herokuapp.com/"
bot = Bot(ACCESS_TOKEN)

# We will receive messages that Facebook sends Stella at this endpoint
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message Stella, Facebook has implemented a verify token
        that confirms all requests that Stella receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)

    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so Stella knows where to send response back to
                recipient_id = message['sender']['id']
                message_text = message['message'].get('text')
                if message_text:
                    """Split parts of the message into tokens.

                    tokens 0 - 'Send'
                    tokens 1 - Public key of receipient
                    tokens 2 - Amount of XLM to send
                    tokens 3 - Private key of sender
                    """
                    tokens = message_text.split(" ")
                    if (tokens[0].upper() == "SEND"):
                        payment_resp = send_payment(tokens)
                        response_sent_text = sent_message(tokens[2], tokens[3])
                        remaining_balance = get_balance(tokens[3])
                        send_message(recipient_id, response_sent_text)
                    else:
                        sender_info = parse_sent_message(message_text)
                        if sender_info:
                            response_sent_text = "My name is Stella. I can help you send Stellar Lumens. " \
                                                 "Please specify the keyword SEND, an amount, recipient, " \
                                                 "and source address."
                            send_message(recipient_id, response_sent_text)
                #if user sends Stella a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = get_invalid_message()
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"

def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def sent_message(amount, name):
    return "Success! You just sent {} XLM to {}".format(amount, name)

def parse_sent_message(tokens):
    if (len(tokens) < 3):
        return
    accountId = tokens[1]
    amount = tokens[2]
    return (accountId, amount,)

#if the user sends something other than a text message
def get_invalid_message():
    return "Invalid message. Please only send lumens"

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

def get_balance(secretSeed):
    req = requests.post(STELLAR_API_URL + "getBalance", {"secretSeed": secretSeed })
    return req.text

def send_payment(tokens):
    if (len(tokens) < 4):
        return "Invalid payment request - not enough arguments"
    dest_acct_id = tokens[1]
    amount = tokens[2]
    secret_seed = tokens[3]
    req = requests.post(STELLAR_API_URL+ "send", {"secretSeed": secret_seed, "destAcctId": dest_acct_id, "amount": amount })
    return req.text

if __name__ == "__main__":
    app.run()
