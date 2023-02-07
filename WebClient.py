import requests
import json
#import Crypto.Random
#from Crypto.Cipher import AES
import hashlib

'''
# salt size in bytes
SALT_SIZE = 16
# number of iterations in the key generation
NUMBER_OF_ITERATIONS = 20
# the size multiple required for AES
AES_MULTIPLE = 16

def generate_key(password, salt, iterations):
    assert iterations > 0
    key = password + salt
    for i in range(iterations):
        key = hashlib.sha256(key).digest()  
    return key

def pad_text(text, multiple):
    extra_bytes = len(text) % multiple
    padding_size = multiple - extra_bytes
    padding = chr(padding_size) * padding_size
    padded_text = text + padding
    return padded_text

def unpad_text(padded_text):
    padding_size = ord(padded_text[-1])
    text = padded_text[:-padding_size]
    return text

def encrypt(plaintext, password):
    salt = Crypto.Random.get_random_bytes(SALT_SIZE)
    key = generate_key(password, salt, NUMBER_OF_ITERATIONS)
    cipher = AES.new(key, AES.MODE_ECB)
    padded_plaintext = pad_text(plaintext, AES_MULTIPLE)
    ciphertext = cipher.encrypt(padded_plaintext)
    ciphertext_with_salt = salt + ciphertext
    return ciphertext_with_salt

def decrypt(ciphertext, password):
    salt = ciphertext[0:SALT_SIZE]
    ciphertext_sans_salt = ciphertext[SALT_SIZE:]
    key = generate_key(password, salt, NUMBER_OF_ITERATIONS)
    cipher = AES.new(key, AES.MODE_ECB)
    padded_plaintext = cipher.decrypt(ciphertext_sans_salt)
    plaintext = unpad_text(padded_plaintext)
    return plaintext
'''
class Client:
    def __init__(self,serverurl):
        self.url = serverurl
    def send_data(self, **data):
        response = requests.post(self.url + 'data/', json = data)
        if response == "Received":
            return 0
        return 1
    def get_data_raw(self):
        data = requests.get(self.url)
        return json.loads(data.text)
    def get_data_var(self, var):
        raw_data = self.get_data_raw()
        try:
            return raw_data[var]
        except Exception as e:
            print("Couldn't get the requested variable: " + str(e))

if __name__ == "__main__":
    URL = "http://localhost:3000/"

    c = Client(URL)
    while True:
        if input("sending or recieving: ") == "sending":
            c.send_data(message=input("Message: "))
        else:
            print(c.get_data_var("message"))