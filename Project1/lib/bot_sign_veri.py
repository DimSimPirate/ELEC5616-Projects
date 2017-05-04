from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
import os

# def gen_key():
#     #for testing
#     rng = Random.new().read
#     key = RSA.generate(2048,rng)
#     key_f=open("../pastebot.net/bots_folder/bot1/sign_public_key.spki","w")
#     key_f.write(key.publickey().exportkey("spki").encode("utf-8"))
#     key_f.close()


# def bot_signfile():
#     # botnet sign files
#     f = open(os.path.join("../pastebot.net/helloworld"),"rd").read()
#     key = RSA.importKey(open('../pastebot.net/sign_public_key.spki').read())
#     hash = SHA256.new(f).digest()
#     signature = PKCS1_v1_5.new(key).sign(hash)
#     return signature


def bot_verification(fn):
    # botnet veri master
    if not os.path.exists(os.path.join("../pastebot.net", fn)):
        print("The given file doesn't exist")
        os._exit(1)
    f = open(os.path.join("../pastebot.net", fn), "r")
    lines = f.readlines()
    f.close()
    h1 = SHA256.new(''.join(lines[:-2]).encode('utf-8'))
    publicKey = RSA.importKey(open('../pastebot.net/public_keys/signature_Public_key.pem').read())
    verifier = PKCS1_v1_5.new(publicKey)
    return verifier.verify(h1, bytes.fromhex(lines[-1]))



