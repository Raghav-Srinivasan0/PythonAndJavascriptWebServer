import requests
import json
import os
#import Crypto.Random
#from Crypto.Cipher import AES
import hashlib
import socket

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
        self.index = -1
        self.url = serverurl
        hostname=socket.gethostname()
        IPAddr=socket.gethostbyname(hostname)
        self.ipaddr = IPAddr
        try:
            ips_raw = requests.get(self.url + 'ips/')
            ips = json.loads(ips_raw.text)['ip']
            ips.append(IPAddr)
            response = requests.post(self.url + 'ip/', json = {'ip': ips})
            self.index = len(ips)-1
        except Exception as e:
            response = requests.post(self.url + 'ip/', json = {'ip': [IPAddr]})
            self.index = 0
    def send_data(self, **data):
        try:
            messages = self.get_data_var("message")
        except Exception as e:
            messages = []
        messages.append(data["message"] + data['ip'])
        response = requests.post(self.url + 'data/', json = {"message": messages})
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
    def get_data_ip(self):
        data = self.get_data_var("message")
        temp_messages = []
        for i in data:
            if i.rfind(self.ipaddr)!=-1:
                temp_messages.append(i[:i.rfind(self.ipaddr)-len(self.ipaddr)])
        return temp_messages
    def get_ips(self):
        ips_raw = requests.get(self.url + 'ips/')
        ips = json.loads(ips_raw.text)['ip']
        temp_ips = []
        for i in ips:
            if i != -1:
                temp_ips.append(i)
        return temp_ips
    def exit(self):
        ips_raw = requests.get(self.url + 'ips/')
        ips = json.loads(ips_raw.text)['ip']
        ips[self.index] = -1
        response = requests.post(self.url + 'ip/', json = {'ip': ips})

if __name__ == "__main__":
    URL = "http://localhost:3000/"

    c = Client(URL)
    while True:
        command = input("Command: ")
        if command == "sending":
            temp_ip = input("For (ip address): ")
            c.send_data(message=input("Message: "),ip=temp_ip)
        if command == "recieving":
            print(c.get_data_var("message"))
        if command.find("file send ") != -1:
            path = command[command.find("file send ")+10:]
            with open(path, "rb") as file:
                data = file.readlines()
            data = b''.join(data)
            c.send_data(file="[" + path + "]" + str(data))
        if command == "file recieve":
            filedata = c.get_data_var("file")
            path = filedata[1:filedata[1:].find("]")+1]
            data = filedata[filedata[1:].find("]")+4:-1]
            try:
                with open(path, "x") as file:
                    # Error: code turns one \r\n into 3 newlines
                    file.write(data.encode().decode('unicode_escape'))
            except Exception as e:
                print("Error in recieving file. " + str(e))
        if command == "ip list":
            print(c.get_ips())
        if command == "exit":
            c.exit()
            break