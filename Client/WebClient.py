import requests
import json

class Client:
    def __init__(self,serverurl):
        self.url = serverurl
    def send_data(self, **data):
        response = requests.post(self.url + 'data', json = data)
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
    c.send_data(data1=1,front="front",ten=10)
    print(c.get_data_var('ten'))