FROM python:3

MAINTAINER buluba89

ADD . /build

RUN cd /build &&\
    pip3 install pipenv &&\
    pipenv install --system &&\
    python setup.py install


VOLUME ["/yatcobot"]

WORKDIR /yatcobot

ENTRYPOINT ["yatcobot"]
CMD []