import os


def update_publickey():

    if os.path.exists('pastebot.net/public_keys/signature_Public_key1.pem.signed'):
        f = open('pastebot.net/public_keys/signature_Public_key1.pem.signed', "rb").read().decode('utf-8')
        file = open("pastebot.net/public_keys/signature_Public_key.pem", 'w')
        tmp = f.splitlines()
        i = 0
        while i <= len(tmp)-3:
            file.write(tmp[i]+'\r')
            i += 1
        file.close()
