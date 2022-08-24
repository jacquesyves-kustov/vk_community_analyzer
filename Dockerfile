FROM python:3.10
MAINTAINER SergeiKustov

ADD . .

RUN pip install --upgrade pip && \
    pip3 install -r requirements.txt

ENTRYPOINT ["python","src/__main__.py"]
