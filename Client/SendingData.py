from WebClient import Client

URL = "http://localhost:3000/"

c = Client(URL)

data_to_send = str(input('Message: '))

c.send_data(msg=data_to_send)