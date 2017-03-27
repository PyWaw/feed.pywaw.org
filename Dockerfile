FROM python:3.6.1

ADD /requirements.txt /requirements.txt

RUN pip install -r requirements.txt

ADD / /

CMD python app.py
