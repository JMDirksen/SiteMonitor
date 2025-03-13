# SiteMonitor
 
Docker container for checking if a site is loading and contains certain text and if the SSL certificate is not expiring. Errors will be send as push notification through [Ntfy.sh](https://ntfy.sh/)


# Environment variables

Variable | Default value | Description
--|--|--
URL | https://example.com | The site URL to check
CONTAINS |  | Text to search for on the site
INTERVAL | 300 | The interval in seconds before testing the site again
TIMEOUT | 3 | Number of seconds to wait for the site to load
SSL_CERT_EXPIRY_DAYS | 28 | Number of days the SSL certificate should still be valid for
NTFY_TOPIC | PortMonitor | The [ntfy topic](https://docs.ntfy.sh/?h=topic#step-1-get-the-app) to send the push notifications to


# Python requirement

```
pip install cryptography
```

# Docker build

```
docker build -t jmdirksen/sitemonitor .
docker push jmdirksen/sitemonitor
```


# Docker run

```
docker run --name sitemonitor --rm -d -e URL=https://example.com -e CONTAINS="Example Domain" jmdirksen/sitemonitor
docker logs -ft sitemonitor
docker stop sitemonitor
```

# Docker compose

```
docker compose up -d
docker compose logs -ft
docker compose down
```
