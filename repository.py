class SubscriptionRepository:
    def __init__(self, db):
        self.db = db

    def create_subscription(self, url):
        query = "insert into subscription(url) values('%s') returning id" %(url)

        new_id = self.db.insert(query)
        return new_id

