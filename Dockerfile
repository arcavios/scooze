# syntax=docker/dockerfile:1

FROM python:3.11
RUN pip install scooze
CMD scooze run
EXPOSE 8000
