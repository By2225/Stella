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

# We will receive messages that Facebook sends our bot at this endpoint
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                print(message)
                message_text = message['message'].get('text')
                if message_text:
                    tokens = message_text.split(" ")
                    if (tokens[0].upper() == "SEND"):
                        payment_resp = send_payment(tokens)
                        print("Payment Sent")
                        print("Payment Response: ", payment_resp)
                        balance_resp = get_balance(tokens[4])
                        print("Balance Response: ", balance_resp)
                        response_sent_text = sent_message(tokens[2], tokens[3])
                        send_message(recipient_id, response_sent_text)
                    else:
                        sender_info = parse_sent_message(message_text)
                        if sender_info:
                            response_sent_text = "My name is Stella. I can help you send Stellar Lumens. " \
                                                 "Please specify the keyword SEND, an amount, recipient, " \
                                                 "and source address."
                            send_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
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
    print(type(recipient_id))
    bot.send_text_message(recipient_id, response)
    return "success"

def get_balance(accountId):
    req = requests.post(STELLAR_API_URL + "getBalance", {"accountId": accountId })
    return req.text

def send_payment(tokens):
    if (len(tokens) < 5):
        print("Invalid payment request - not enough arguments")
        return
    dest_acct_id = tokens[1]
    print(dest_acct_id)
    amount = tokens[2]
    secret_seed = tokens[3]
    req = requests.post(STELLAR_API_URL+ "send", {"secretSeed": secret_seed, "destAcctId": dest_acct_id, "amount": amount })
    return req.text

if __name__ == "__main__":
    app.run()
