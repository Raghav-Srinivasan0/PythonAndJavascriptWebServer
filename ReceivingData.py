from WebClient import Client

URL = "http://localhost:3000/"

c = Client(URL)

print(c.get_data_raw())