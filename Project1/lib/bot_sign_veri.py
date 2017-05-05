from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
import os


def bot_verification(fn):
    # botnet veri master
    lines = fn.decode('utf-8').splitlines()
    h1 = SHA256.new(''.join(lines[:-2]).encode('utf-8'))
    print (''.join(lines[:-2]).encode('utf-8'))
    if not os.path.exists('pastebot.net/public_keys/signature_Public_key.pem'):
        print("There is not public key installed in public_keys folder, run master_bot and type command"
              " 'generate-key' to upload a new one")
        os._exit(1)
    publicKey = RSA.importKey(open('pastebot.net/public_keys/signature_Public_key.pem').read())
    verifier = PKCS1_v1_5.new(publicKey)
    print (h1.hexdigest())
    print (''.join(lines[:-2]).encode('utf-8'))
    try:
        sign = bytes.fromhex(lines[-1])
        return verifier.verify(h1, sign)
    except ValueError:
        return False


