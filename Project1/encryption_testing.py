from Crypto.Cipher import AES

IV = "1234567890123456"
Key = "12345678901234567890123456789012"

cipher_1 = AES.new(Key,AES.MODE_CFB,IV)
cipher_2 = AES.new(Key,AES.MODE_CFB,IV)
cipher_2_temp = AES.new(Key,AES.MODE_CFB,IV)
cipher_3 = AES.new(Key,AES.MODE_CFB,IV)

msg = "Hello bot."

print("Try to encrypt--encrypt msg")
print("1. The encrypt: {}".format(cipher_1.encrypt(msg)))
print("2. The encrypt: {}".format(cipher_1.encrypt(msg)))

print(">>>>>>")
print("Try to encrypt--decrypt--encrypt msg")
c2 = cipher_2_temp.encrypt(msg) # using cipher_2_temp to avoid corruption of iv0 of cipher_2
print("1. The encrypt with iv0: {}".format(c2))
print("2. The decrypt with iv0: {}".format(cipher_2.decrypt(c2))) # now the status of cipher_2 should be iv1
print("3. The encrypt with iv1: {}".format(cipher_2.encrypt(msg))) # compare this with line 27

print(">>>>>>")
print("Try to encrypt--encrypt msg")
print("1. The encrypt with iv0: {}".format(cipher_3.encrypt(msg)))
print("2. The encrypt with iv1: {}".format(cipher_3.encrypt(msg))) # compare this with lin 22
