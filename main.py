from client import Client
from image import generate_image
from task import createtask, starttask
client = Client()
client.login()

def main(client):
    generate_image()
    client.imagepost(".images/result.png")

taskobj = createtask(client, main, client).start()
starttask(client, taskobj)