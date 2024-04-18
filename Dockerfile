# syntax=docker/dockerfile:1

FROM python:3.11
RUN pip install git+https://github.com/arcavios/scooze@dev#egg=scooze
CMD scooze run
EXPOSE 8000
