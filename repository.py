class SubscriptionRepository:
    def __init__(self, db):
        self.db = db

    def create_subscription(self, url):
        query = "insert into subscription(url) values('%s') returning id" %(url)
        new_id = self.db.insert(query)
        return new_id

    def get_all_subscriptions(self):
        query = "SELECT url, id FROM subscription"
        all_subscriptions = self.db.query(query)
        return all_subscriptions

    def delete_subscriptions(self, id):
        query = "DELETE FROM subscription WHERE id = %s" %id
        all_subscriptions = self.db.update(query)
        return all_subscriptions
