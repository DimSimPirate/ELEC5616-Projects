from Crypto.Hash import SHA256
from Crypto.Random import random
from lib.helpers import read_hex
from dh import RFC_3526

# Project TODO: Is this the best choice of prime? Why? Why not? Feel free to replace!

# 6144-bit safe prime for Diffie-Hellman key exchange
# obtained from RFC 3526
# Convert from the value supplied in the RFC to an integer

# Project TODO: write the appropriate code to perform DH key exchange
def prime_select(commu):
    raw_prime = ''
    if commu == '1536-bit' or commu == '':
        raw_prime = RFC_3526.raw_prime_1536
    elif commu == '2048-bit':
        raw_prime = RFC_3526.raw_prime_2048
    elif commu == '3072-bit':
        raw_prime = RFC_3526.raw_prime_3072
    elif commu == '4096-bit':
        raw_prime = RFC_3526.raw_prime_4096
    elif commu == '6144-bit':
        raw_prime = RFC_3526.raw_prime_6144
    elif commu == '8192-bit':
        raw_prime = RFC_3526.raw_prime_8192
    return raw_prime

def create_dh_key(commu):
    # Generator is always 2
    g = 2

    # Get the corresponding prime
    raw_prime = prime_select(commu)
    prime = read_hex(raw_prime)

    # Returns (public, private)
    private = random.randint(2, prime-2)
    public = pow(g, private, prime)
    return (public, private)

def calculate_dh_secret(their_public, my_private, commu):

    # Calculate the shared secret
    raw_prime = prime_select(commu)
    prime = read_hex(raw_prime)
    shared_secret = pow(their_public, my_private, prime)

    # Hash the value so that:
    # (a) There's no bias in the bits of the output
    #     (there may be bias if the shared secret is used raw)
    # (b) We can convert to raw bytes easily
    # (c) We could add additional information if we wanted
    # Feel free to change SHA256 to a different value if more appropriate
    shared_hash = SHA256.new(bytes(str(shared_secret), "ascii")).hexdigest()
    return shared_hash
