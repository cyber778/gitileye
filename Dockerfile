FROM python:3.9
ENV PYTHONUNBUFFERED=1
WORKDIR /django
ADD . /django
COPY requirements/base.txt requirements.txt
RUN pip3 install -r requirements.txt