from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto import Random
import os

# def gen_key():
#     #for testing
#     rng = Random.new().read
#     key = RSA.generate(2048,rng)
#     key_f=open("../pastebot.net/bots_folder/bot1/sign_public_key.spki","w")
#     key_f.write(key.publickey().exportkey("spki").encode("utf-8"))
#     key_f.close()


def bot_signfile():
    #botnet sign files
    f = open(os.path.join("../pastebot/bots_folder/bot1/helloworld"),"rd").read()
    key = RSA.importKey(open('../pastebot/bots_folder/bot1/sign_public_key.spki').read())
    hash = SHA256.new(f).digest()
    signature = PKCS1_v1_5.new(key).sign(hash)
    return signature



def bot_verification(rec_file):
    #botnet veri master
    publickey=RSA.importKey(open('../pastebot.net/bots_folder/bot1/signature_Public_key.pem').read())
    veri =PKCS1_v1_5.new(rec_file, publickey)
    if veri:
        print("the file comes from master")
    else:
        print("it does not come from master")



