
# Using (PKCS #1 v1.5) signature algorithm
# as mentioned in https://www.dlitz.net/software/pycrypto/api/current/Crypto.Cipher.PKCS1_v1_5-module.html

from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import os
import binascii

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

    #TODO: handle file not found exception so the program doesnt have to exit
    # Make sure the path is exist
    if not os.path.exists(os.path.join("pastebot.net", file_path)):
        print("There is not such file or directory, try again:")
        return 0

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
        return 0

    # Read the key stored in the master_folder
    key = RSA.importKey(open('master_folder/signature_Private_key.pem').read())

    # sign the file
    # attach the signature on at the end of file
    # return bytes stream
    sign = PKCS1_v1_5.new(key)
    signature = sign.sign(h)

    hex_bytes = binascii.hexlify(signature)
    hex_str = hex_bytes.decode("ascii")

    #signature.hex() only works in python 3.5
    #f_signed = file_data+"\nSignature: \n" + signature.hex()
    f_signed = file_data+"\nSignature: \n" + hex_str
    return f_signed

def update_pubkey():
   # generate a new key with private and write it in the file
    key = RSA.generate(2048)
    f = open("master_folder/signature_Private_key1.pem",'w')
    f.write(key.exportKey('PEM').decode('utf-8'))
    f.close()

    # public generation
    f = open("master_folder/signature_Public_key1.pem", 'w')
    f.write(key.publickey().exportKey('PEM').decode('utf-8'))
    f.close()

    f = open('master_folder/signature_Public_key1.pem', "rb")
    file_data = f.read().decode('utf-8')
    #print(file_data)

    oldprikey = RSA.importKey(open('master_folder/signature_Private_key.pem').read())
    sign = PKCS1_v1_5.new(oldprikey)
    h = SHA256.new(''.join(file_data).encode('utf-8'))
    signature = sign.sign(h)
    hex_bytes = binascii.hexlify(signature)
    hex_str = hex_bytes.decode("ascii")
    f_signed = file_data + "\nSignature: \n" + hex_str
    # write the new key to master signature private key
    f = open("master_folder/signature_Private_key.pem", 'w')
    f.write(key.exportKey('PEM').decode('utf-8'))
    f.close()
    return f_signed