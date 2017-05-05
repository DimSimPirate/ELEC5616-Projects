# ELEC5616-Projects

## Why there two different cipher-text when using `p2p echo`?
### Problem are demonstrated in following:
```
Listening on port 1337
Waiting for connection...
Enter command: p2p echo
Finding another bot...
Found bot on port 1338
Shared hash: 6d77c67147fa243c8d768e79a2b55f8d5a30e391a10fc82139cd885204479a95
Original data: b'ECHO'
Encrypted data: b'\x97@T\xf1'
Sending packet of length 4
--------
problem is following
--------
Echo> hello bob!
Original data: b'hello bob!'
Encrypted data: b'l\xf8\xe9\xf3\xc4=/\xd4\x91q'
Sending packet of length 10
Receiving packet of length 10
Encrypted data: b'5\x1e\x12\xe6\xb3\xee\x1fZ"\xcd'
Original data: b'hello bob!'
```
Lets suppose this is **Alice** talking to **Bob**, and the echo procedure is following:

msg --> Alice's cipher-text --> Bob --> Bob's decryption --> msg --> Bob's cipher-text --> Alice --> Alice's decryption -->msg

The common sense is that, the Alice's cipher-text should equal to Bob's cipher-text, because they are encrypting the same msg.

### Explanation (More demon is in the `encryption-tesitng.py`):
We are using the **ASE_CFB** method to encrypt msg, so that we should provide the same IV(initial vector) to Alice and Bob. Lets suppose its *IV0*.


1. As Alice encrypted msg with IV0, her crypto will change the initial vector to IV1 (this is bound in the encryption-method to avoid duplicate msg generates the same cipher-text).

2. Then Bob decrypted cipher-text with IV0, his crypto will change the initial vector to IV1, which is the same as Alice's IV1 (so they are on the same page).

3. Bob send the encrypted cipher-text back to Alice with VI1 (**This is the reason why the two cipher-texts are not the same, because the first cipher-text is encrypted with IV0, but the second is encrypted with IV1**), and Bob's initial vector switch to IV2.

4. Alice received the cipher-text, decrypted it with IV1, and got the msg. Her initial vector switch to IV2 which is the same as Bob's.

5. Repeating above stages

## Pycharm show error with "unsolved reference", even if you can run the code

1. Right click the `Project1` folder in pycharm

2. Find the option `Mark directory as`, and choose the `Sources Root`

## Part 2 Implementation:

### Signature demo
```
(elec5616) ➜  Project1 git:(impl-bot-verification) ✗ python master_view.py
Waiting for your command, master :3 generate-key
key-pair generated successfully! and uploaded to pastebot.net
Waiting for your command, master :3 sign Secrete1
signed successfully
Waiting for your command, master :3 view Secrete1.signed
there is no secrete... :3
Signature:
50bd0638c9316d4ddb3b006ea5a1bb4e579667376e243a303c0ac6bff69e01e02d324f410d7908cfaca02f290753d1e47e72fe6a435da8878cc124b845ea76d8e1072c282589c9846bf2b1160cab838eb3b2bf93c38808a2cf440b6118adc918fd1b71c4a52661034642ca2d929da1b8b23af4329eb64225088e1a02b5648c09c22efc10fa0821368ebc80a120804a6a7566c558d82e0e75e35200f6d94960d12c58da6f96b9cdfef3efa481cf6c9b65af078e98dabdf74d7ee6e19f3c15ca4a5121e31ebb2af28f1bc4eceea4698041062e33365bfacaa05f601f7239a43c80d7a265b898f252082a266e21045dca76789f625646d547f9a154031eccb9f5fd

=== The bot side ===
(elec5616) ➜  Project1 git:(impl-bot-verification) ✗ python bot.py
Listening on port 1337
Waiting for connection...
Enter command: download Secrete1.signed
Stored the received file as Secrete1.signed
Enter command: download Secrete1
The file has not been signed by the botnet master
Enter command:
```

### Encryption demo
```
=== The bot side ===
(elec5616) ➜  Project1 git:(impl-master-decryption) ✗ python bot.py
Listening on port 1337
Waiting for connection...
Enter command: mine
Mining for Bitcoins...
-
Mined and found Bitcoin address: 3nyD8iI2xHzPZDqjtefRKqSJKo6dgcf9xC4
Enter command: harvest
Found user pass: ('Ben', 'xMauV4yP')
Enter command: list
Files stored by this bot:
Valuables stored by this bot: ['Bitcoin: 3nyD8iI2xHzPZDqjtefRKqSJKo6dgcf9xC4', 'Username/Password: Ben xMauV4yP']
Enter command: upload testing_upload
Saved valuables to pastebot.net/testing_upload for the botnet master

== The master side ===
(elec5616) ➜  Project1 git:(impl-master-decryption) ✗ python master_view.py
Waiting for your command, master :3 view testing_upload
Bitcoin: 3nyD8iI2xHzPZDqjtefRKqSJKo6dgcf9xC4
Username/Password: Ben xMauV4yP
```