FROM python:slim

ARG TAG=latest

COPY main.py /
COPY database.py /
COPY demo-portfolio.csv /
COPY assets/ /assets/

RUN pip install pandas
RUN pip install dash
RUN pip install dash-auth
RUN pip install requests

EXPOSE 8085/tcp

CMD python main.py