# syntax=docker/dockerfile:1

# ref: https://stackoverflow.com/a/57886655

FROM debian:12-slim AS builder
RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes pipx
ENV PATH="/root/.local/bin:${PATH}"
RUN pipx install poetry
RUN pipx inject poetry poetry-plugin-bundle
WORKDIR /src
COPY . .
RUN poetry bundle venv --python=/usr/bin/python3 --only=main /venv

FROM gcr.io/distroless/python3-debian12
COPY --from=builder /venv /venv
ENTRYPOINT ["/venv/bin/scooze"]

# TODO: how do I do this with the given entry point or do I need a diff entry point? etc
# CMD ["uvicorn", "scooze.main:app", "--host", "127.0.0.1", "--port", "8000"]
# scooze run
CMD ["run"]

EXPOSE 8000
