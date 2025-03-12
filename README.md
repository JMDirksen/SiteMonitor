# SiteMonitor
 
Docker container checking if sites are loading and contains sertain text and if the SSL certificate is not expiring, errors will be send as push notification through [Ntfy.sh](https://ntfy.sh/)


# Environment variables

Variable | Default value | Description
--|--|--
URL | http://example.com | The site URL to check
CONTAINS |  | Text to search for on the site
INTERVAL | 300 | The interval in seconds before testing the site again
TIMEOUT | 3 | Number of seconds to wait for a connection to be made
SSL_CERT_EXPIRY_DAYS | 28 | Number of days the SSL certificate should still be valid for
NTFY_TOPIC | PortMonitor | The [ntfy topic](https://docs.ntfy.sh/?h=topic#step-1-get-the-app) to send the push notifications to


# Build

```
docker build -t jmdirksen/sitemonitor .
docker push jmdirksen/sitemonitor
```


# Run

```
docker run --name sitemonitor --rm -d -e URL=https://example.com -e CONTAINS="Example Domain" jmdirksen/sitemonitor
docker logs -ft sitemonitor
docker stop sitemonitor
```

# Compose

```
docker compose up -d
docker compose logs -ft
docker compose down
```
