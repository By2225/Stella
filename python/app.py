#Python libraries that we need to import for our bot
#https://www.twilio.com/blog/2017/12/facebook-messenger-bot-python.html
import random
import requests
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = 'ACCESS_TOKEN'
VERIFY_TOKEN = 'VERIFY_TOKEN'
bot = Bot(ACCESS_TOKEN)
app.url_map.strict_slashes = False

@app.route("/", methods=['GET', 'POST'])
def welcome():
    return "You have connected to the Facebook Messenger Bot"

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/receive_msg/", methods=['GET', 'POST'])
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
       #print("hello")
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    response_sent_text = get_message()
                    send_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message()
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"

@app.route("/send/<secret_seed>/<dest_acct_id>/<amount>/", methods=['POST'])
def send_payment(secret_seed, dest_acct_id, amount):
    root_url = "http://d1663146.ngrok.io/send/"
    req = requests.post(root_url, {"secretSeed": secret_seed, "destAcctId":dest_acct_id, "amount": amount })
    return req.text

@app.route("/balance/<accountId>/", methods=['POST'])
def get_balance(accountId):
    root_url = "http://d1663146.ngrok.io/getBalance/"
    req = requests.post(root_url, {"accountId": accountId })
    return req.text

def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

@app.route("/register_testnet_acct/<accountId>/", methods=['POST'])
def register_testnet_acct(accountId):
    root_url = "http://d1663146.ngrok.io/registerTestNetAccount/"
    req = requests.post(root_url, {"accountId": accountId })
    return req.text

@app.route('/create_key_pair/', methods=['GET', 'POST'])
def create_key_pair():
    root_url = "http://d1663146.ngrok.io/createKeyPair/"
    req = requests.post(root_url)
    return req.text





#chooses a random message to send to the user
def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()
