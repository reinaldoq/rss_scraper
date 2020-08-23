from celery import Celery
import os
import requests


app = Celery('tasks',backend='rpc://', broker='pyamqp://guest@'+os.environ['BROKER_HOST']+'//')

@app.task
def update_subscription():
    #db y traer listado de subscripciones,
    #select id,url from subscription
    subscriptions = [
        {'url': 'http://www.nu.nl/rss/Algemeen',
        'id':1},
        {'url':'https://feeds.feedburner.com/tweakers/mixed',
         'id':2}
    ]
    for s in subscriptions:
        new_data = download(s['url'])
        store_data(s['id'], new_data)


def download(url):
    return requests.get(url)

def store_data(id_subscription, new_data):
    #guardr esto en db
    for d in new_data:
        #insert into subscription_data crear esta tabal nueva
        pass


#terminar todos los endpoints
#crear las tablas que falta, tablas apra datos y tabla de config
#terminar el job de celery para descargar los datos
# - conectar a la db y conseguir lista de todas als subscripciones
# - descargar el contenido del rss y parsearlo a modo texto
# - guardar la data en la db
