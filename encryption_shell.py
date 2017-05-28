from __future__ import print_function
import sys
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

# Bind input to raw_input for Python 2 support
try:
   input = raw_input
except NameError:
   pass

class AESCipher(object):

    def __init__(self, key): 
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

f = open("shared_secret.txt", "r")
secret = f.readlines()[0].strip()
aesCipher = AESCipher(secret)

while True:
    print("Choose action: Encryption[e]/Decryption[d]")
    command = input()
    if command == "e":
        print("Insert message to encrypt:")
        message = input()
        ciphertext = aesCipher.encrypt(message)
        ciphertext = str(ciphertext)
        # Remove stuff in version 3
        if ciphertext[:2] == "b'":
            ciphertext = ciphertext[2:-1]
        print("\n" + ciphertext + "\n")
    elif command == "d":
        print("Insert cyphertext to decrypt:")
        ciphertext = input()
        message = aesCipher.decrypt(ciphertext)
        print("\n" + message + "\n")