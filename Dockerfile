FROM python:latest
RUN apt-get install -y git
RUN git clone https://github.com/MaKla89/PortfolioAnalyser

RUN pip install pandas
RUN pip install dash
RUN pip install requests

EXPOSE 8085/tcp

WORKDIR /PortfolioAnalyser
CMD python main.py