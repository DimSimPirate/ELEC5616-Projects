
# Using (PKCS #1 v1.5) signature algorithm
# as mentioned in https://www.dlitz.net/software/pycrypto/api/current/Crypto.Cipher.PKCS1_v1_5-module.html

from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from binascii import unhexlify
import os


def generate_key():
    # Using RSA to generate 2048-bit keys
    key = RSA.generate(2048)

    # Write the private key
    f = open("master_folder/signature_Private_key.pem",'w')
    f.write(key.exportKey('PEM').decode('utf-8'))
    f.close()

    # Write the public key
    f = open("master_folder/signature_Public_key.pem",'w')
    f.write(key.publickey().exportKey('PEM').decode('utf-8'))
    f.close()

    # Upload the public key
    f = open("pastebot.net/public_keys/signature_Public_key.pem",'w')
    f.write(key.publickey().exportKey('PEM').decode('utf-8'))
    f.close()

def sign_file(file_path):
    # sign the file with signature
    # print(file.read().encode('utf-8'))
    # generate_key()
    if not os.path.exists(os.path.join("pastebot.net", file_path)):
        print("There is not such file or director, try again:")
        os._exit(1)
    f = open(os.path.join("pastebot.net/", file_path), "rb")
    file_data = f.read().decode('utf-8')
    f.close()

    lines = file_data.split('\n')
    h = SHA256.new(''.join(lines).encode('utf-8'))
    if not os.path.exists('master_folder/signature_Private_key.pem'):
        print("you do not have a key-pair, enter 'generate-key' command to get one")
        os._exit(1)
    key = RSA.importKey(open('master_folder/signature_Private_key.pem').read())
    sign = PKCS1_v1_5.new(key)
    signature = sign.sign(h)
    f_signed = file_data+"\nSignature: \n" + signature.hex()
    return f_signed


# Demonstrate the sign and verify process
# master side generation
# if __name__ == "__main__":
#     # file = input("input a file to sign: ")
#     file = input("Which file do you want to sign master? ")
#     sign_file(file)
#     # bot side verification
#     if not os.path.exists(os.path.join("../master_folder/", file)):
#         print("There is not such file or director, try again:")
#         os._exit(1)
#     f = open(os.path.join("../master_folder/", file), "rb")
#     file_data = f.read()
#     lines = file_data.decode('utf-8').split('\n')
#     f.close()
#     h1 = SHA256.new(''.join(lines[:-2]).encode('utf-8'))
#     publicKey = RSA.importKey(open('../pastebot.net/public_keys/signature_Public_key.pem').read())
#     verifier = PKCS1_v1_5.new(publicKey)
#     if verifier.verify(h1,bytes.fromhex(lines[-1])):
#         print("verified")
#     else:
#         print("not verified")
#

