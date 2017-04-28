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
