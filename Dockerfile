FROM jupyter/scipy-notebook

RUN apt-get update && apt-get install -yq libmysqlclient-dev

ADD requirements.txt ./requirements.txt
RUN /bin/bash -c "source activate python2 && pip install -r requirements.txt"

ENV PATH /nyse-demo:$PATH
ADD . /home/jovyan/work
RUN chown -R jovyan:users /home/jovyan
