
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
    f = open("../master_folder/signature_Private_key.pem",'w')
    f.write(key.exportKey('PEM').decode('utf-8'))
    f.close()

    # Write the public key
    f = open("../master_folder/signature_Public_key.pem",'w')
    f.write(key.publickey().exportKey('PEM').decode('utf-8'))
    f.close()

def sign_file(file_path):
    # sign the file with signature
    # print(file.read().encode('utf-8'))
    # generate_key()
    if not os.path.exists(os.path.join("../master_folder/", file_path)):
        print("There is not such file or director, try again:")
        os._exit(1)
    f = open(os.path.join("../master_folder/", file_path), "r")
    lines = f.readlines()
    h = SHA256.new(''.join(lines).encode('utf-8')+b'\n')
    f.close()
    key = RSA.importKey(open('../master_folder/signature_Private_key.pem').read())
    sign = PKCS1_v1_5.new(key)
    signature = sign.sign(h)
    f = open(os.path.join("../master_folder/", file_path), "a")
    f.write("\nSignature: \n" + signature.hex())
    f.close()

    ## TODO: This is a dummy upload for testing signature, need to submit it through the net
    f = open(os.path.join("../master_folder/", file_path), "r")
    f_w = open(os.path.join("../pastebot.net/", file_path), "w")
    f_w.write(f.read())
    f.close()
    f_w.close()

# Demonstrate the sign and verify process
# master side generation
if __name__ == "__main__":
    # file = input("input a file to sign: ")
    file = 'hello.signed'
    sign_file(file)
    # bot side verification
    if not os.path.exists(os.path.join("../master_folder/", file)):
        print("There is not such file or director, try again:")
        os._exit(1)
    f = open(os.path.join("../master_folder/", file), "r")
    lines = f.readlines()
    f.close()
    h1 = SHA256.new(''.join(lines[:-2]).encode('utf-8'))
    publicKey = RSA.importKey(open('../pastebot.net/public_keys/signature_Public_key.pem').read())
    verifier = PKCS1_v1_5.new(publicKey)
    if verifier.verify(h1,bytes.fromhex(lines[-1])):
        print("verified")
    else:
        print("not verified")
#

