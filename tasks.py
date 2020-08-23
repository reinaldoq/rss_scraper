from celery import Celery
import os
import requests
from repository import SubscriptionRepository
from provider_postgres import PostgresProvider



app = Celery('tasks',backend='rpc://', broker='pyamqp://guest@'+os.environ['BROKER_HOST']+'//')

#@app.task
def update_subscription():
    db = PostgresProvider(
        os.environ['POSTGRES_USER'],
        os.environ['POSTGRES_PASSWORD'],
        os.environ['POSTGRES_HOST'],
        os.environ['POSTGRES_DB'])

    db.connect()
    repository = SubscriptionRepository(db)
    subscriptions = repository.get_all_subscriptions()

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
