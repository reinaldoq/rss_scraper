import os
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from celery import Celery

from provider_postgres import PostgresProvider
from repository import SubscriptionRepository

# app = Celery('tasks', backend='rpc://', broker='pyamqp://guest@' + os.environ['BROKER_HOST'] + '//')


def scrap_feed(articles, subscription_id):
    articles_in_subscription = []

    # for each "item" I want, parse it into a list
    for a in articles:
        title = a.find('title').text.replace("'", " ")
        link = a.find('link').text
        published_wrong = a.find('pubDate').text
        published = datetime.strptime(published_wrong, '%a, %d %b %Y %H:%M:%S %z')
        description = a.find('description').text.replace("'", " ")

        # print(published, published_wrong) # checking correct date format

        # create an "article" object with the data
        # from each "item"
        article = {
            'subscription_id': subscription_id,
            'title': title,
            'link': link,
            'published': published,
            'description': description
        }

        # append my "article_list" with each "article" object
        articles_in_subscription.append(article)

    return articles_in_subscription

def scraper():
    db = PostgresProvider(
        os.environ['POSTGRES_USER'],
        os.environ['POSTGRES_PASSWORD'],
        os.environ['POSTGRES_HOST'],
        os.environ['POSTGRES_DB'])

    db.connect()
    repository = SubscriptionRepository(db)
    subscriptions = repository.get_all_subscriptions()

    try:
        for s in subscriptions:
            # execute my request, parse the data using XML
            # parser in BS4
            r = requests.get(s[0])
            soup = BeautifulSoup(r.content, features='xml')

            # select only the "items" I want from the data
            articles = soup.findAll('item')

            articles_in_subscription = scrap_feed(articles, s[1])

            repository.insert_subscription_item(articles_in_subscription)

        return 0

        # return save_function(article_list)
    except Exception as e:
        print('The scraping job failed. See exception:')
        print(e)

# terminar todos los endpoints
# crear las tablas que falta, tablas apra datos y tabla de config
# terminar el job de celery para descargar los datos
# - conectar a la db y conseguir lista de todas als subscripciones
# - descargar el contenido del rss y parsearlo a modo texto
# - guardar la data en la db
