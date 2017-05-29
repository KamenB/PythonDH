from __future__ import print_function
import sys
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

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

if __name__ == '__main__':
    # Bind input to raw_input for Python 2 support
    try:
       input = raw_input
    except NameError:
       pass

    # Fetch secrets database
    f = open("shared_secrets.txt", "r")
    secrets = [x.strip().split(",") for x in f.readlines()]
    f.close()
    l = "Select correspondant:\n"
    for i, secret in enumerate(secrets):
        l += secret[0] + ": " + str(i) + "\n"
    print(l)
    
    # Wait for correct correspondent choice
    while True:
        try:
            j = int(input())
        except ValueError:
            print("Please enter a number in the provided range")
            continue
        if j < 0 or j >= len(secrets):
            print("Please enter a number in the provided range")
            continue
        break
    print("Correspondant chosen: " + secrets[j][0])
    secret = secrets[j][1]

    # Construct cipher object
    aesCipher = AESCipher(secret)

    # Begin encryption/decryption shell
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