import os
from lib.master_sign import generate_signkey, sign_file,update_pubkey
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto import Random

def decrypt_valuables(f):
    # TODO: For Part 2, you'll need to decrypt the contents of this file

    # Extracting the hash and content
    h_rec = f[-64:]
    data_ency = f[:-64]

    # Generate the hash by ourselves and make sure its valid, otherwise we will drop it
    h_veri = SHA256.new(data_ency)
    dsize = SHA256.digest_size
    sentinel = Random.new().read(15 + dsize)

    # make sure the hash is valid
    if h_veri.hexdigest() == h_rec.decode('utf-8'):

        # make sure the path is valid
        if not os.path.exists("master_folder/encryption_Private_key.pem"):
            print("there is not Private key, try to run 'generate-encykey' to get one")
        else:
            # extract the private key from master_folder
            key = RSA.importKey(open("master_folder/encryption_Private_key.pem").read())
            cipher = PKCS1_v1_5.new(key)

            # Decrypt the data
            decrypted_data = cipher.decrypt(data_ency, sentinel)
            print(decrypted_data.decode('utf-8'))

    else:
        print("Ah!!!!! The file be modified by SOMEONE!!!! Or, It's not encrypted so sad :(")

def generate_encykey():

    key = RSA.generate(2048)

    # Write the private key
    f = open("master_folder/encryption_Private_key.pem",'w')
    f.write(key.exportKey('PEM').decode('utf-8'))
    f.close()

    # Write the public key
    f = open("master_folder/encryption_Public_key.pem",'w')
    f.write(key.publickey().exportKey('PEM').decode('utf-8'))
    f.close()

    # Upload the public key to pastebot.net/public_keys
    f = open("bot_localfiles/encryption_Public_key.pem",'w')
    f.write(key.publickey().exportKey('PEM').decode('utf-8'))
    f.close()

# This is for master_view controller, master can enter command to do some features:
# - help (list of all commands available)
# - generate-signkey (to generate the signature key)
# - generate-encykey (to generate the encryption key)
# - sign FILENAME (to sign a file in the pastebot.net)
# - view FILENAME (to decrypt and print it out of a file in the pastebot,net)
# - cat FILENAME (observe the content of a plaintext file, caution: cannot use for encrypted file)
# - quit / exit (exit the program)
if __name__ == "__main__":
    print("Welcome master, type help for a list of commands")
    while 1:
        raw_cd = input("Waiting for your command, master :3 ")
        cmd = raw_cd.split()
        if not cmd:
            print("Dear master, you need to enter a command :3")
            continue

        if cmd[0].lower() == 'help':
            print('-- help (list of all commands available)')
            print('-- list (lists all files in pastebot.net)')
            print('-- generate-signkey (to generate the signature key)')
            print('-- generate-encykey (to generate the encryption key)')
            print('-- sign FILENAME (to sign a file in the pastebot.net)')
            print('-- view FILENAME (to decrypt a file in the pastebot.net, uploaded from a bot')
            print('-- cat FILENAME (observe the content of a plaintext file, caution: cannot use for encrypted file)')
            print('-- create FILENAME (create a plaintext file, contents specified by user input, and sign)')
            print('-- quit / exit (exit the program)')
            print('-- upubk (update the public key)')

        elif cmd[0].lower() == 'list':
            for fname in os.listdir('pastebot.net'):
                # ignore the public_keys directory
                if fname == 'public_keys':
                    continue
                print(fname)

        elif cmd[0].lower() == 'generate-signkey':
            generate_signkey()
            print("Signature key-pair generated successfully! and uploaded to bot_localfiles")

        elif cmd[0].lower() == 'generate-encykey':
            generate_encykey()
            print("Encyption key-pair generated successfully! and uploaded to bot_localfiles")

        elif cmd[0].lower() == 'sign':
            if len(cmd) == 2:
                fn = cmd[1]
                f_signed = sign_file(fn)
                # Proceed if no errors signing file
                if f_signed != 0:
                    f = open(os.path.join("pastebot.net", fn+'.signed'), 'w')
                    f.write(f_signed)
                    f.close()
                    print("signed successfully")
            else:
                print("The sign command requires a filename afterwards")

        elif cmd[0].lower() == 'view':
            if len(cmd) == 2:
                fn = cmd[1]
                if not os.path.exists(os.path.join("pastebot.net", fn)):
                    print("The given file doesn't exist on pastebot.net")
                else:
                    f = open(os.path.join("pastebot.net", fn), "rb").read()
                    decrypt_valuables(f)
            else:
                print("The view command requires a filename afterwards")

        elif cmd[0].lower() == 'cat':
            if len(cmd) == 2:
                fn = cmd[1]
                if not os.path.exists(os.path.join("pastebot.net", fn)):
                    print("The given file doesn't exist on pastebot.net")
                else:
                    f = open(os.path.join("pastebot.net", fn), "rb").read()
                    try:
                        print(str(f, 'ascii'))
                    except ValueError:
                        print("nah, I guess there are some hex our of 0-127 range")
            else:
                print("The view command requires a filename afterwards")

        elif cmd[0].lower() == 'create':
            if len(cmd) == 2:
                fn = cmd[1]
                # NOTE: not entirely secure, raw file will be visible for a short time
                # TODO: create a temporary file inside master_folder instead
                raw_file = open(os.path.join('pastebot.net', fn),"w+")
                raw_txt = input("Enter the text you wish to write into the file: ")
                raw_file.write(raw_txt)
                raw_file.close()
                signed_file = sign_file(fn)

                if signed_file != 0:
                    f = open(os.path.join("pastebot.net", fn+'.signed'), 'w')
                    f.write(signed_file)
                    f.close()
                    print("Signed file successfully created")

                os.remove(os.path.join('pastebot.net', fn))

            else:
                print("WHAT THE HELL MAN, I CANT MAKE A FILE WITHOUT A NAME")

        elif cmd[0].lower() == 'upubk':
            f_signed = update_pubkey()
            f = open(os.path.join("bot_localfiles", "signature_Public_key1.pem" + '.signed'), 'w')
            f.write(f_signed)
            f.close()
            print("the public key has changed")

        elif cmd[0].lower() == "quit" or cmd[0].lower() == "exit":
            break

        else:
            print("ahh, invalid command")
