import os
from lib.master_sign import generate_key, sign_file


def decrypt_valuables(f):
    # TODO: For Part 2, you'll need to decrypt the contents of this file
    # The existing scheme uploads in plaintext
    # As such, we just convert it back to ASCII and print it out
    decoded_text = str(f, 'ascii')
    print(decoded_text)


if __name__ == "__main__":
    while 1:
        raw_cd = input("Waiting for your command, master :3 ")
        cmd = raw_cd.split()
        if not cmd:
            print("Dear master, you need to enter a command :3")
            continue

        if cmd[0].lower() == 'generate-key':
            generate_key()
            print("key-pair generated successfully! and uploaded to pastebot.net")

        elif cmd[0].lower() == 'sign':
            if len(cmd) == 2:
                fn = cmd[1]
                f_signed = sign_file(fn)
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
                    os._exit(1)
                f = open(os.path.join("pastebot.net", fn), "rb").read()
                decrypt_valuables(f)
            else:
                print("The view command requires a filename afterwards")

        elif cmd[0].lower() == "quit" or cmd[0].lower() == "exit":
            break

        else:
            print("ahh, invalid command")
