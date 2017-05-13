from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
import os

def bot_verification(fn):
    # botnet verify master
    lines = fn.decode('utf-8').splitlines()

    # The true content is stored in first to -2nd lines
    # Hash it for verification
    h1 = SHA256.new(''.join(lines[:-2]).encode('utf-8'))

    # Make sure the path is valid
    if not os.path.exists('bot_localfiles/signature_Public_key.pem'):
        print("There is not public key installed in public_keys folder, run master_bot and type command"
              " 'generate-signkey' to upload a new one")
    else:
        # Extract public keys from pastebot.net/public_keys
        publicKey = RSA.importKey(open('bot_localfiles/signature_Public_key.pem').read())

        # Verifying the data
        verifier = PKCS1_v1_5.new(publicKey)

        # The 'bytes.fromhex()' sometimes fails,
        # that is because when you are trying to treat a plaintext as a signature,
        # the range of plaintext is out of range of Hex.
        # Using try except to make sure the program is solid
        try:
            sign = bytes.fromhex(lines[-1])
            return verifier.verify(h1, sign)
        except ValueError:
            return False
