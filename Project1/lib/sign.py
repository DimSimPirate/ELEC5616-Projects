
# Using (PKCS #1 v1.5) signature algorithm
# as mentioned in https://www.dlitz.net/software/pycrypto/api/current/Crypto.Cipher.PKCS1_v1_5-module.html

from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto import Random
from Crypto.PublicKey import RSA


def generate_key():
    # Using RSA to generate 2048-bit keys
    key = RSA.generate(2048)

    # Write the key to master_folder/signature_key.pem
    f = open("../pastebot.net/master_folder/signature_Private_key.pem",'w')
    f.write(key.exportKey('PEM').decode('utf-8'))
    f.close()



def sign_file(file):
    pass