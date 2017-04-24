FROM python:3.6.1

ADD /requirements.txt /requirements.txt

RUN pip install -r requirements.txt

ADD / /

CMD python -m aiohttp.web -H 0.0.0.0 -P 8000 feed.app:create_app
