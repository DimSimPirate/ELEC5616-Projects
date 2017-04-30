import struct

from Crypto.Cipher import AES
from Crypto.Hash import HMAC
from Crypto.Random import random
from Crypto.PublicKey import DSA

from dh import create_dh_key, calculate_dh_secret

# Global variable storing used nonces
nonces = []

class StealthConn(object):
    def __init__(self, conn, client=False, server=False, verbose=False, show_handshake=True):
        self.conn = conn
        self.cipher = None
        self.h = None
        #self.signature = None
        self.client = client
        self.server = server
        self.verbose = verbose
        self.show_handshake = show_handshake
        self.initiate_session()

    def initiate_session(self):
        # Perform the initial connection handshake for agreeing on a shared secret

        if self.client:
            # Ask user to input the MODP, damn yeah you can choose any prime from RFC 3526
            # Keep asking until you make it correct
            while 1:
                commu = input('Choose a MODP group (default 1536), '
                              'valid inputs are "1536-bit", "2048-bit", "3072-bit", "4096-bit", "6144-bit", "8192-bit": ')
                if commu == '' or commu == '1536-bit' or commu == '2048-bit' or commu == '3072-bit' or commu == '4096-bit' or commu == '6144-bit' or commu == '8192-bit':
                    break
                else:
                    print('invalid input, try again:')

            # Create the dh_key by your input
            my_public_key, my_private_key = create_dh_key(commu)

            # Send them our public key and your choice to server, so that server can know which MODP to use
            # Split it by a space ' ', for better distinction on the server side
            msg = str(my_public_key)+' '+commu
            self.send(bytes(msg, "ascii"))

            # Receive their public key
            their_public_key = int(self.recv())

            # If you want to have a clear demo of shake-hand, make show_handshake = True can help you
            if self.show_handshake:
                print("The first shake-hand: {}".format(msg))
                print("Received public key: {}".format(their_public_key))

            # Obtain our shared secret
            shared_hash = calculate_dh_secret(their_public_key, my_private_key, commu)
            print("Shared hash: {}".format(shared_hash))

        if self.server:

            # We should receive the msg first, which contain the MODP and client's public key
            shake1 = self.recv()

            # Demo the shake-hand procedure
            if self.show_handshake:
                print("The received first handshake: {}".format(shake1))

            # Split the received msg by ' ', then we can use it for different purpose
            shake1 = shake1.split(b' ')

            # The client's public key is the first [0] element
            # The MODP info is the second [1] element
            their_public_key = int(shake1[0])
            commu = shake1[1].decode('utf-8')

            # Generate public and private key, and send it to client
            my_public_key, my_private_key = create_dh_key(commu)
            self.send(bytes(str(my_public_key), "ascii"))
            # Obtain our shared secret
            shared_hash = calculate_dh_secret(their_public_key, my_private_key, commu)
            print("Shared hash: {}".format(shared_hash))

        # TODO 2: Optimize the IV and key for more security
        # TODO 3: For the block cipher, it requires fix message length, we need to write a padding and unpadding function.

        # By using the shared_key, we can make a MAC and cipher.
        # In here, we use the HMAC, and the CFB mode of AES as the cipher
        IV = shared_hash[:16]
        key = shared_hash[:32]
        secrete = bytes(shared_hash, 'ascii')

        # Using AES.OFB cipher
        # NOTE: Perhaps change the encryption mode depending on key selection to match secuity requirements
        self.cipher = AES.new(key, AES.MODE_CFB, IV)

        # using HMAC
        self.h = HMAC.new(secrete)

        # Signature generation
        # sigKey = DSA.generate(1024)

    def send(self, data):
        if self.cipher and self.h:
            # TODO: include a timestamp so that nonces dont have to be stored forever
            # NOTE: timestamp must be encrypted, otherwise attacker can use previous message but make the time valid

            # Attached nonce, lengthened to 10 digits
            nonce = random.StrongRandom().getrandbits(24)

            encrypted_data = self.cipher.encrypt(str(nonce).zfill(10).encode() + data)
            self.h.update(encrypted_data)

            # HMAC the cipher-text
            attached_hmac = bytes(self.h.hexdigest(),'ascii')

            # Attached the HMAC on the front
            encrypted_data = attached_hmac + encrypted_data

            # Attached digital signature
            #randK = random.StrongRandom().randint(1, self.sigKey.q-1)
            #atached_sig = self.key.sign(encrypted_data, randK)
            #encrypted_data = encrypted_data + attached_sig

            if self.verbose:
                print("sending HMAC: {}".format(attached_hmac)) # Display the HMAC value on the sender-side
                print("Original data: {}".format(data))
                print("Encrypted data: {}".format(repr(encrypted_data)))
                print("Sending packet of length {}".format(len(encrypted_data)))
        else:
            encrypted_data = data

        # Encode the data's length into an unsigned two byte int ('H')
        pkt_len = struct.pack('H', len(encrypted_data))
        self.conn.sendall(pkt_len)
        self.conn.sendall(encrypted_data)

    def recv(self):
        # Decode the data's length from an unsigned two byte int ('H')
        pkt_len_packed = self.conn.recv(struct.calcsize('H'))
        unpacked_contents = struct.unpack('H', pkt_len_packed)
        pkt_len = unpacked_contents[0]

        encrypted_data = self.conn.recv(pkt_len)
        if self.cipher and self.h:
            # Grape the header HMAC and calculate HMAC
            attached_hmac = encrypted_data[:32]
            self.h.update(encrypted_data[32:])
            calculated_hmac = bytes(self.h.hexdigest(),'ascii')

            # Grape the cipher-text and decipher
            data = self.cipher.decrypt(encrypted_data[32:])
            message = data[10:]
            nonce = data[:10]
            if self.verbose:
                print("Receiving packet of length {}".format(pkt_len))
                print("Encrypted data: {}".format(repr(encrypted_data)))
                print("Original data: {}".format(data))
                print("Calculated HMAC: {}".format(calculated_hmac))
                print("Attached HMAC: {}".format(attached_hmac))
                if attached_hmac == calculated_hmac:
                    print("HMAC verified, have a good day~!")
                else:
                    print("Someone modified the message, take care!")
                print("Nonce: {}".format(nonce))
                if (nonce in nonces):
                    print("Nonce already used, be wary of replay attack!")
                else:
                    print("Valid nonce, noice")
                    nonces.append(nonce)
        else:
            message = encrypted_data

        return message

    def close(self):
        self.conn.close()
