# syntax=docker/dockerfile:1
# ref: https://stackoverflow.com/a/57886655

FROM python:3-slim AS builder
RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes pipx
ENV PATH="/root/.local/bin:$PATH"
RUN pipx install poetry
RUN pipx inject poetry poetry-plugin-bundle
WORKDIR /src
COPY . .
RUN poetry bundle venv --python=/usr/bin/python3 --only=main /venv

# Adding :debug to the image uses the published version of the container image
# that contains debug tools (like /bin/bash) to be able to get into the
# container and poke around
FROM gcr.io/distroless/python3-debian12:debug
COPY --from=builder /venv /venv
ENTRYPOINT ["/venv/bin/scooze", "run"]

EXPOSE 8000
