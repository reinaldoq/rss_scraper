from flask import Flask
from flask import request
from repository import SubscriptionRepository
import json
import os
from provider_postgres import PostgresProvider
from tasks import update_subscription

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
            'row': subscription_list,
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
    result = update_subscription()
    """while not result.ready()
        print(result.ready())
        print(result.backendc)"""

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

    #id = request.args.get('id')
    repository = SubscriptionRepository(db)
    deleted = repository.delete_subscriptions(id)
    response = {
        'data': deleted
    }


    return app.response_class(status=201, mimetype='application/json', response=json.dumps(response))
