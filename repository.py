class SubscriptionRepository:
    def __init__(self, db):
        self.db = db

    def create_subscription(self, url):
        query = "insert into subscription(url) values('%s') returning id" % url
        new_id = self.db.insert(query)
        return new_id

    def get_all_subscriptions(self):
        query = "SELECT url, id FROM subscription"
        all_subscriptions = self.db.query(query)
        return all_subscriptions

    def delete_subscriptions(self, item_id):
        query = "DELETE FROM subscription WHERE id = %s" % item_id
        all_subscriptions = self.db.update(query)
        return all_subscriptions

    def insert_subscription_item(self, items_list):
        for i in items_list:
            subscription_id = i['subscription_id']
            title = i['title']
            link = i['link']
            published = i['published']
            description = i['description']
            query = """insert into items(
            subscription_id, 
            title, 
            link, 
            published, 
            description
            ) values(%d, '%s', '%s', '%s', '%s') returning id""" % (
                subscription_id,
                title,
                link,
                published,
                description)
            self.db.insert(query)

        return 0

    def get_feed(self, subscription_id, filter_items):
        if filter_items:
            filter_items = filter_items.lower()

        query = "SELECT id, title, read FROM items"
        connector = 'where'

        if subscription_id:
            connector = 'and'
            query = query + ' where subscription_id=%s' % subscription_id

        if filter_items == 'read':
            query = query + ' %s read=true' % connector

        if filter_items == 'unread':
            query = query + ' %s read=false' % connector

        feed = self.db.query(query)
        return feed

    def read_item(self, item_id):
        query = "UPDATE items set read=true where id=%s" % item_id
        feed = self.db.update(query)
        return feed
