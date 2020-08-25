import os
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from celery import Celery

from provider_postgres import PostgresProvider
from repository import SubscriptionRepository


# To fix
# app = Celery('tasks', backend='rpc://', broker='pyamqp://guest@' + os.environ['BROKER_HOST'] + '//')

# Parse function
def scrap_feed(articles, subscription_id):
    articles_in_subscription = []

    # Extract info for each article
    for a in articles:
        title = a.find('title').text.replace("'", " ")
        link = a.find('link').text
        published_wrong = a.find('pubDate').text
        published = datetime.strptime(published_wrong, '%a, %d %b %Y %H:%M:%S %z')
        description = a.find('description').text.replace("'", " ")

        # Save it in a article object
        article = {
            'subscription_id': subscription_id,
            'title': title,
            'link': link,
            'published': published,
            'description': description
        }

        # Append article to the list
        articles_in_subscription.append(article)

    # Return the list with all articles
    return articles_in_subscription


# The Scraper itself
def scraper():
    # Connect to the db
    db = PostgresProvider(
        os.environ['POSTGRES_USER'],
        os.environ['POSTGRES_PASSWORD'],
        os.environ['POSTGRES_HOST'],
        os.environ['POSTGRES_DB'])

    db.connect()
    repository = SubscriptionRepository(db)
    # Get all the subscription to scrap from
    subscriptions = repository.get_all_subscriptions()

    try:
        for s in subscriptions:
            # Request all item info
            r = requests.get(s[0])
            # Parse it
            soup = BeautifulSoup(r.content, features='xml')

            # Select just the part needed
            articles = soup.findAll('item')

            # Pass the articles and the subscription id to convert it in an article object
            articles_in_subscription = scrap_feed(articles, s[1])

            # Insert it into the db
            repository.insert_subscription_item(articles_in_subscription)

        return 0

    # If something goes wrong it raises an exception
    except Exception as e:
        print('Error in the scraping process:')
        print(e)
