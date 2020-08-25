class SubscriptionRepository:
    def __init__(self, db):
        self.db = db

    # Create a new subscription in db
    def create_subscription(self, url):
        query = "insert into subscription(url) values('%s') returning id" % url
        new_id = self.db.insert(query)
        return new_id

    # Return the url and id of all subscriptions in db
    def get_all_subscriptions(self):
        query = "SELECT url, id FROM subscription"
        all_subscriptions = self.db.query(query)
        return all_subscriptions

    # First deletes the items associated with a subscriptions
    # After deletes the subscription
    def delete_subscriptions(self, item_id):
        query = "DELETE FROM items WHERE subscription_id = %s" % item_id
        self.db.update(query)
        query = "DELETE FROM subscription WHERE id = %s" % item_id
        del_subscriptions = self.db.update(query)
        return del_subscriptions

    # Inserts a item for each element of a given list of items
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

    # Returns feed filtered or unfiltered depending on what arguments are provide
    def get_feed(self, subscription_id, filter_items):
        # Set filter to lower to prevent db errors
        if filter_items:
            filter_items = filter_items.lower()

        # The basic query with no filter or id return all the items
        query = "SELECT id, title, read FROM items"
        connector = 'where'

        # If an iD is provide is added to the query
        if subscription_id:
            connector = 'and'
            query = query + ' where subscription_id=%s' % subscription_id

        # If filter is set to read is added to the query
        if filter_items == 'read':
            query = query + ' %s read=true' % connector

        # If filter is set to unread is added to the query
        if filter_items == 'unread':
            query = query + ' %s read=false' % connector

        feed = self.db.query(query)
        return feed

    # Update read to true of a specific item
    def read_item(self, item_id):
        query = "UPDATE items set read=true where id=%s" % item_id
        feed = self.db.update(query)
        return feed
