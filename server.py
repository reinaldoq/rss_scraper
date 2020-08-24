from flask import Flask
from flask import request
from repository import SubscriptionRepository
import json
import os
from provider_postgres import PostgresProvider
from tasks import update_subscription
from tasks import scraper
from tasks import scraper

app = Flask(__name__)


@app.route('/api/v1/subscription')
def get_subscription():
    db = PostgresProvider(
        os.environ['POSTGRES_USER'],
        os.environ['POSTGRES_PASSWORD'],
        os.environ['POSTGRES_HOST'],
        os.environ['POSTGRES_DB'])

    db.connect()
    repository = SubscriptionRepository(db)
    all_subscriptions = repository.get_all_subscriptions()

    subscription_list = []

    for s in all_subscriptions:
        rsp = {
            'url': s[0],
            'id': s[1]
        }

        subscription_list.append(rsp)

    response = {
        'data': subscription_list,
    }


    return app.response_class(status=200, mimetype='application/json', response=json.dumps(response))


@app.route('/api/v1/subscription', methods=['POST'])
def add_subscription():
    db = PostgresProvider(
        os.environ['POSTGRES_USER'],
        os.environ['POSTGRES_PASSWORD'],
        os.environ['POSTGRES_HOST'],
        os.environ['POSTGRES_DB'])

    db.connect()
    body = request.json
    url = body['url']
    repository = SubscriptionRepository(db)
    new_id = repository.create_subscription(url)
    response = {
        'data': new_id
    }

    return app.response_class(status=201, mimetype='application/json', response=json.dumps(response))


@app.route('/api/v1/subscription/update', methods=['POST'])
def update_subscription_content():
    result = scraper()

    response = {
        'data': result
    }

    return app.response_class(status=200, mimetype='application/json', response=json.dumps(response))


@app.route('/api/v1/subscription/<id>', methods=['POST'])
def delete_subscription(id):
    db = PostgresProvider(
        os.environ['POSTGRES_USER'],
        os.environ['POSTGRES_PASSWORD'],
        os.environ['POSTGRES_HOST'],
        os.environ['POSTGRES_DB'])

    db.connect()

    # id = request.args.get('id')
    repository = SubscriptionRepository(db)
    deleted = repository.delete_subscriptions(id)
    response = {
        'data': deleted
    }

    return app.response_class(status=201, mimetype='application/json', response=json.dumps(response))

@app.route('/api/v1/feed/<subscription_id>', methods=['GET'])
def all_feed(subscription_id):
    return all_feed_by_id(subscription_id)


def all_feed_by_id(subscription_id):
    db = PostgresProvider(
        os.environ['POSTGRES_USER'],
        os.environ['POSTGRES_PASSWORD'],
        os.environ['POSTGRES_HOST'],
        os.environ['POSTGRES_DB'])

    db.connect()

    filter_items = request.args.get('filter', None)

    repository = SubscriptionRepository(db)
    feed = repository.get_feed(subscription_id, filter_items)

    feed_list = []

    for s in feed:
        rsp = {
            'id': s[0],
            'title': s[1],
            'read': s[2]
        }

        feed_list.append(rsp)

    response = {
        'data': feed_list,
    }

    return app.response_class(status=200, mimetype='application/json', response=json.dumps(response))


@app.route('/api/v1/feed', methods=['GET'])
def all_feed_no_id():
    return all_feed_by_id(None)


@app.route('/api/v1/item/<item_id>/read', methods=['POST'])
def read_item(item_id):
    db = PostgresProvider(
        os.environ['POSTGRES_USER'],
        os.environ['POSTGRES_PASSWORD'],
        os.environ['POSTGRES_HOST'],
        os.environ['POSTGRES_DB'])

    db.connect()

    repository = SubscriptionRepository(db)
    deleted = repository.read_item(item_id)
    response = {
        'data': deleted
    }

    return app.response_class(status=201, mimetype='application/json', response=json.dumps(response))

