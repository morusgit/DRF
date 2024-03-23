FROM python:3

WORKDIR /code_mls

COPY ./requirements.txt /code_mls

RUN pip install -r /code_mls/requirements.txt

COPY . .