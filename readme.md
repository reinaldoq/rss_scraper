#RSS Scraper
Simple API service to scrap RSS feeds and obtain items from those feeds.

**Production deployment**
Generate Docker image from Dockerfile
`docker build -t rq/api-scraper:latest .
`
Create a container exposing port 5000.

Initialize database with the file in:
`rss_scraper/docker-entrypoint-initdb.d/create_db.sql`

Name the database rssfeeed

Initialize environment variables:
`POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_HOST
POSTGRES_DB`

**Commands**
Start service
'docker-compose up
'
Stop service
'docker-compose down
'
Start service with no logs
'docker-compose up -d 
'
Start service watching api/db logs
docker-compose logs -f api/db

**Endpoints**
Consult all existing subscriptions_
GET /api/v1/subscription
```angular2html
OUTPUT
{
    url: <Feed's URL>
    id: <Subscription ID>
}
```

Add a new subscription
POST /api/v1/subscription
```angular2html
INPUT BODY
{
    url: <Feed's URL>
}
```

Delete existing subscription
POST /api/v1/subscription/<Subscription ID>

Update all subscriptions
POST /api/v1/subscription/update

GET /api/v1/feed/<Subscription ID>
```angular2html
PARAMETERS: 
    Filter: read/unread/If not provide returns globally

OUTPUT:
    [{
    id: Feed item unique ID.
    text: Item text.
    status: Read/Unread
    }]
```

Mark item as read
POST /api/v1/item/<Item ID>/read
