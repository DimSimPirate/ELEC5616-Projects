
# Using (PKCS #1 v1.5) signature algorithm
# as mentioned in https://www.dlitz.net/software/pycrypto/api/current/Crypto.Cipher.PKCS1_v1_5-module.html

from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto import Random
from Crypto.PublicKey import RSA
import os

def generate_key():
    # Using RSA to generate 2048-bit keys
    key = RSA.generate(2048)

    # Write the private key
    f = open("../pastebot.net/master_folder/signature_Private_key.pem",'w')
    f.write(key.exportKey('PEM').decode('utf-8'))
    f.close()

    # Write the public key
    f = open("../pastebot.net/master_folder/signature_Public_key.pem",'w')
    f.write(key.publickey().exportKey('PEM').decode('utf-8'))
    f.close()

def sign_file(file):
    # sign the file with signature
    # print(file.read().encode('utf-8'))
    f = open(os.path.join("../pastebot.net/master_folder/", file), "rb").read()
    h = SHA256.new(f)
    print(h.hexdigest())
    key = RSA.importKey(open('../pastebot.net/master_folder/signature_Private_key.pem').read())
    sign = PKCS1_v1_5.new(key)
    signature = sign.sign(h)

    return signature

# Demonstrate the sign and verify process
# master side generation
# file = 'hello.fbi'
#
# f = open(os.path.join("../pastebot.net/master_folder/", file), "rb").read()
# h1 = SHA256.new(f)
# print(h1.hexdigest())
# signature = sign_file(file)
#
#
#
# # bot side verification
# publicKey = RSA.importKey(open('../pastebot.net/master_folder/signature_Public_key.pem').read())
# verifier = PKCS1_v1_5.new(publicKey)
# if verifier.verify(h1,signature):
#     print("verified")
# else:
#     print("not verified")
# #

