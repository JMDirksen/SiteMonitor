FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV URL=https://example.com
ENV INTERVAL=300
ENV TIMEOUT=3
ENV NTFY_TOPIC="SiteMonitor"

CMD [ "python", "./run.py" ]
