FROM python:3.9-alpine
WORKDIR /code
COPY pyproject.toml .
RUN addgroup -S appgroup && adduser --no-create-home -S appuser -G appgroup && \
    chown appuser:appgroup /code && \
    apk add --no-cache gcc musl-dev libffi-dev && \
    pip install poetry fastapi starlette_exporter redis && \
    poetry install
COPY src src
USER appuser
CMD [ "python", "-u", "./src/api.py" ]
