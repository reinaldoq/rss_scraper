import json
import os

from flask import Flask
from flask import request

from provider_postgres import PostgresProvider
from repository import SubscriptionRepository
from tasks import scraper

app = Flask(__name__)


# Endpoint to consult all subscriptions
@app.route('/api/v1/subscription')
def get_subscription():
    # Connect with db
    db = PostgresProvider(
        os.environ['POSTGRES_USER'],
        os.environ['POSTGRES_PASSWORD'],
        os.environ['POSTGRES_HOST'],
        os.environ['POSTGRES_DB'])

    db.connect()
    repository = SubscriptionRepository(db)
    # Execute the method returning all subscriptions in db
    all_subscriptions = repository.get_all_subscriptions()

    subscription_list = []

    # Parse the url and id of each subscription and add it to the list
    for s in all_subscriptions:
        rsp = {
            'url': s[0],
            'id': s[1]
        }

        subscription_list.append(rsp)

    # Put the list in data and return it
    response = {
        'data': subscription_list,
    }

    return app.response_class(status=200, mimetype='application/json', response=json.dumps(response))


# Endpoint to add a new subscription
@app.route('/api/v1/subscription', methods=['POST'])
def add_subscription():
    # Connect with db
    db = PostgresProvider(
        os.environ['POSTGRES_USER'],
        os.environ['POSTGRES_PASSWORD'],
        os.environ['POSTGRES_HOST'],
        os.environ['POSTGRES_DB'])

    db.connect()
    # Get the url param from the body of the message
    body = request.json
    url = body['url']
    repository = SubscriptionRepository(db)
    # Pass that url as a argument to the create subscription method of the repository
    new_id = repository.create_subscription(url)
    # Response with the new id of the subscription
    response = {
        'data': new_id
    }

    return app.response_class(status=201, mimetype='application/json', response=json.dumps(response))


# Endpoint to update an specific subscription
# There lives the scraper functionality
# Ideally this should connect with a Celery task
@app.route('/api/v1/subscription/update', methods=['POST'])
def update_subscription_content():
    # Call scraper function, if works return 0
    result = scraper()

    response = {
        'data': result
    }

    return app.response_class(status=200, mimetype='application/json', response=json.dumps(response))


# Endpoint to delete a subscription
@app.route('/api/v1/subscription/<subscription_id>', methods=['POST'])
def delete_subscription(subscription_id):
    # Connect to db
    db = PostgresProvider(
        os.environ['POSTGRES_USER'],
        os.environ['POSTGRES_PASSWORD'],
        os.environ['POSTGRES_HOST'],
        os.environ['POSTGRES_DB'])

    db.connect()
    repository = SubscriptionRepository(db)

    # Calls the delete method in the repository
    deleted = repository.delete_subscriptions(subscription_id)
    response = {
        'data': deleted
    }

    return app.response_class(status=201, mimetype='application/json', response=json.dumps(response))


# The filter endpoint
@app.route('/api/v1/feed/<subscription_id>', methods=['GET'])
# If a subscription ID is provided we call the all filter by id function
def all_feed(subscription_id):
    return all_feed_by_id(subscription_id)


# This function returns all items of a subscription given a subscription ID
def all_feed_by_id(subscription_id):
    # Connect to db
    db = PostgresProvider(
        os.environ['POSTGRES_USER'],
        os.environ['POSTGRES_PASSWORD'],
        os.environ['POSTGRES_HOST'],
        os.environ['POSTGRES_DB'])

    db.connect()

    # Catch the filter param from the url
    # If not, it is set to None
    filter_items = request.args.get('filter', None)

    repository = SubscriptionRepository(db)

    # Pass the subscription ID and filter params to the get feed function
    feed = repository.get_feed(subscription_id, filter_items)

    feed_list = []

    # Parse the id, title and read status of the items
    for s in feed:
        rsp = {
            'id': s[0],
            'title': s[1],
            'read': s[2]
        }

        feed_list.append(rsp)

    # Return all items in the list
    response = {
        'data': feed_list,
    }

    return app.response_class(status=200, mimetype='application/json', response=json.dumps(response))


# Returns items globally
@app.route('/api/v1/feed', methods=['GET'])
# Pass None as an argument to all feed by id function
def all_feed_no_id():
    return all_feed_by_id(None)


# Function to set items as read
@app.route('/api/v1/item/<item_id>/read', methods=['POST'])
def read_item(item_id):
    # Connect to db
    db = PostgresProvider(
        os.environ['POSTGRES_USER'],
        os.environ['POSTGRES_PASSWORD'],
        os.environ['POSTGRES_HOST'],
        os.environ['POSTGRES_DB'])

    db.connect()

    repository = SubscriptionRepository(db)
    # Pass the item id to the read item function in the repository
    read = repository.read_item(item_id)
    # Returns all the feed with the item read to True
    response = {
        'data': read
    }

    return app.response_class(status=201, mimetype='application/json', response=json.dumps(response))
