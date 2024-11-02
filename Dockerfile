FROM python:slim

ARG TAG=latest

COPY main.py /
COPY database.py /
COPY data/ /data/
COPY assets/ /assets/

RUN pip install pandas
RUN pip install dash
RUN pip install dash-auth
RUN pip install requests
RUN pip install waitress
RUN pip install yahoofinancials

EXPOSE 8085/tcp

CMD python main.py