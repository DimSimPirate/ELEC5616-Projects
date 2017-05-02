
# Using (PKCS #1 v1.5) signature algorithm
# as mentioned in https://www.dlitz.net/software/pycrypto/api/current/Crypto.Cipher.PKCS1_v1_5-module.html

from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto import Random
from Crypto.PublicKey import RSA


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
    h = SHA256.new(file.encode('utf-8'))
    key = RSA.importKey(open('../pastebot.net/master_folder/signature_Private_key.pem').read())
    sign = PKCS1_v1_5.new(key)
    signature = sign.sign(h)

    return signature

# Demonstrate the sign and verify process
generate_key()
file = 'signed msg'
h = SHA256.new(file.encode('utf-8'))
abc = sign_file(file)
publicKey = RSA.importKey(open('../pastebot.net/master_folder/signature_Public_key.pem').read())
print(abc)
verifier = PKCS1_v1_5.new(publicKey)
if verifier.verify(h,abc):
    print("verified")
else:
    print("not verified")


