import requests

class Client:
    def __init__(self,serverurl):
        self.url = serverurl
    def send_data(self, **data):
        response = requests.post(self.url, json = data)
        if response == "Received":
            return 0
        return 1
    def get_data(self):
        return requests.get(self.url)

if __name__ == "__main__":
    URL = "http://localhost:3000/data"

    c = Client(URL)
    c.send_data(data1=1,front="front",ten=10)