# Stella
A Facebook Messenger bot for sending Stellar Lumens

# Inspiration:
Stellar lumens is a cryptocurrency that allows for near-instant global payments for only a fraction of a cent. With current financial systems, such as Western Union and MoneyGram, participants have to pay steep fee's and often have to wait up to 3 business days to receive the money. To highlight the great features of Stellar lumens, we wanted to create an interface that simplifies the ability to send lumens across borders utilizing Facebook messenger.

# Functionality:
Interact with the Stellar network through Facebook Messenger Main features
  * Send lumens
  * Check account balance
  * Create and verify new account
  
# Sketch view: 

  
# How we built it:
The application is built using two web microservices:
  1. Python Flask microservice: interfaces with Facebook Messenger and directly processes user messages.
  2. Java Spring microservice: connects the Stellar network to send lumens and monitor accounts.

# Challenges we faced:
* Setting up environment with IntelliJ, Gradel, and Spring
* Sending HTTP requests using Ngrok
* Debugging app in Heroku
* Sending and receiving texts via Facebook messenger
* Facebook developer account approval

# Accomplishments:
* Deploying Python Flask microservice using Heroku
* Using Gradel for Java builds
* Deploying first Java Web microservice with Spring
* Successfully interfacing with Stellar Java SDK

# What we learned:
* How to create messenger bot 
* How to use Gradel
* Spring microservices
* Ngrok
* Heroku
* Flask

# Future of Stella:
* Secure private keys using encryption
* Link public account ids to Facebook profile pseudonyms
* Deploy app on Stellar main-net
* Develop more robust text message parser
* Better integrate Python and Java microservices
* Send output message to receiver for payment confirmation
* Feature for displaying recent transaction history
