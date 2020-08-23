from flask import Flask
from flask import request
from repository import SubscriptionRepository
import json
import os
from provider_postgres import PostgresProvider
from tasks import add
app = Flask(__name__)


@app.route('/')
def hello():
    return 'HELLO'


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
        'data':new_id
    }


    return app.response_class(status=201, mimetype='application/json', response=json.dumps(response))


@app.route('/api/v1/subscription/update', methods=['POST'])
def update_subscription_content():
    result = add.delay(4, 4)
    """while not result.ready():
        print(result.ready())
        print(result.backendc)"""


    response = {
        'data':'OK'
    }


    return app.response_class(status=200, mimetype='application/json', response=json.dumps(response))


