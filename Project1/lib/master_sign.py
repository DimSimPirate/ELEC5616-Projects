
# Using (PKCS #1 v1.5) signature algorithm
# as mentioned in https://www.dlitz.net/software/pycrypto/api/current/Crypto.Cipher.PKCS1_v1_5-module.html

from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import os


def generate_signkey():
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

    # Upload the public key to pastebot.net/public_keys
    f = open("pastebot.net/public_keys/signature_Public_key.pem",'w')
    f.write(key.publickey().exportKey('PEM').decode('utf-8'))
    f.close()


def sign_file(file_path):

    # Make sure the path is exist
    if not os.path.exists(os.path.join("pastebot.net", file_path)):
        print("There is not such file or director, try again:")
        os._exit(1)

    # Read the file and store it as bytes
    f = open(os.path.join("pastebot.net/", file_path), "rb")
    file_data = f.read().decode('utf-8')

    # close the file, the data is stored in file_data
    f.close()

    # split the file in lines, this is mirrored as the bot try to verifying the signature.
    # just in order to make sure they are on the same page.
    lines = file_data.splitlines()

    # hash it.
    h = SHA256.new(''.join(lines).encode('utf-8'))

    # Make sure the path is valid
    if not os.path.exists('master_folder/signature_Private_key.pem'):
        print("you do not have a key-pair, enter 'generate-signKey' command to get one")
        os._exit(1)

    # Read the key stored in the master_folder
    key = RSA.importKey(open('master_folder/signature_Private_key.pem').read())

    # sign the file
    # attach the signature on at the end of file
    # return bytes stream
    sign = PKCS1_v1_5.new(key)
    signature = sign.sign(h)
    f_signed = file_data+"\nSignature: \n" + signature.hex()
    return f_signed


