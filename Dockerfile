FROM python:2.7.10-wheezy

RUN apt-get update && apt-get install -y gfortran liblapack-dev libmysqlclient-dev \
    python-numpy python-scipy python-matplotlib python-imaging-tk python-sympy \
    python-nose libfreetype6-dev

ADD Makefile README.md best.py gen.py plot.py regress.py requirements.txt schema.sql /nyse-demo/

WORKDIR /nyse-demo
RUN virtualenv venv
RUN . venv/bin/activate
RUN pip install -r requirements.txt
