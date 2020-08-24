/api/v1/
GET /api/v1/subscription
```angular2html
OUTPUT
{
    url: <Feed's URL>
    id: <Subscription ID>
}
```
POST /api/v1/subscription
```angular2html
INPUT BODY
{
    url: <Feed's URL>
}
```
DELETE /api/v1/subscription/<Subscription ID>

POST /api/v1/subscription/update

GET /api/v1/feed/<Subscription ID>
```angular2html
PARAMETERS: 
    Filter: Read/Unread/All

OUTPUT:
    [{
    id: Feed item unique ID.
    text: Item text.
    status: Read/Unread
    }]
```
POST /api/v1/item/<Item ID>/read


#COMMANDS
docker-compose up
docker-compose down
docker-compose up -d 
docker-compose logs -f api


