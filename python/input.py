#Takes in user input and returns the http request link
# 
import string
input_str = input("Enter the Account Id, Secret Seed, and Amount: ") 
#AccountID/GC46JFTQCIEYVWCLUD3WHCIITUBTSSSOXQ3BFWU3OVYOFLRSJKHXJUQC
#/SecretSeed/SAGKPY3PZAPZHHCVVGUMYX2VDTGB2QZL3OWQGSZOCQPSDF5G7SWOTVG4
#/Amount/10

list = []

list = input_str.split("/")
#print(list)
str_account = list[0]
str_seed = list[1]
str_amount = list[2]

request = "http://d1663146.ngrok.io/send?secretSeed={}&destAcctId={}&amount={}".format(str_account, str_seed, str_amount)
print(request)