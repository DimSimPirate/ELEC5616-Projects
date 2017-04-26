import struct

from Crypto.Cipher import AES
from Crypto.Hash import HMAC

from dh import create_dh_key, calculate_dh_secret

class StealthConn(object):
    def __init__(self, conn, client=False, server=False, verbose=False):
        self.conn = conn
        self.cipher = None
        self.h = None
        self.client = client
        self.server = server
        self.verbose = verbose
        self.initiate_session()

    def initiate_session(self):
        # Perform the initial connection handshake for agreeing on a shared secret

        ### TODO: Your code here!
        # This can be broken into code run just on the server or just on the client
        if self.server or self.client:
            my_public_key, my_private_key = create_dh_key()
            # Send them our public key
            self.send(bytes(str(my_public_key), "ascii"))
            # Receive their public key
            their_public_key = int(self.recv())
            # Obtain our shared secret
            shared_hash = calculate_dh_secret(their_public_key, my_private_key)
            print("Shared hash: {}".format(shared_hash))

        # Default XOR algorithm can only take a key of length 32

        # Using AES.OFB cipher
        # TODO 2: Optimize the IV and key for more security
        # TODO 3: For the block cipher, it requires fix message length, we need to write a padding and unpadding function.
        IV = shared_hash[:16]
        key = shared_hash[:32]
        secrete = bytes(shared_hash, 'ascii')
        self.cipher = AES.new(key, AES.MODE_CFB, IV)
        self.h = HMAC.new(secrete)

    def send(self, data):
        if self.cipher and self.h:
            encrypted_data = self.cipher.encrypt(data)
            self.h.update(encrypted_data)
            attached_hmac = bytes(self.h.hexdigest(),'ascii')       # HMAC the cipher-text
            encrypted_data = attached_hmac + encrypted_data         # Attached the HMAC on the front
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
            attached_hmac = encrypted_data[:32]             # Grape the header HMAC
            self.h.update(encrypted_data[32:])
            calculated_hmac = bytes(self.h.hexdigest(),'ascii')    # Calculate the hmac value
            data = self.cipher.decrypt(encrypted_data[32:]) # Grape the cipher-text and decipher
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
        else:
            data = encrypted_data

        return data

    def close(self):
        self.conn.close()
