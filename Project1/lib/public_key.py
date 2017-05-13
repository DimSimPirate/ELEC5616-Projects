import os


def publickey():

    if os.path.exists('pastebot.net/public_keys/signature_Public_key1.pem.signed'):
        f = open('pastebot.net/public_keys/signature_Public_key1.pem.signed',"rb").read().decode('utf-8')
        file = open("pastebot.net/public_keys/signature_Public_key.pem", 'w')
        # line = f.readlines()
        tmp = f.splitlines()
        leng=len(tmp)
        i=0
        while i<=leng-3:
            file.write(tmp[i]+'\r')
            i=i+1

        file.close()
    # else :
    #     #os.path.exists('pasterbot.net/public_keys/signature_Public_key.pem'):
    #     f2 =open ('pastebot.net/public_keys/signature_Public_key.pem','rb').read().decode('utf-8')
    #     tmp2 = f2.splitlines()
    #     leng2 = len(tmp2)
    #     j=1
    #     while j<=leng2-2:
    #         str=str+tmp2[j]
    #         j=j+1
    print("publickey has read")
