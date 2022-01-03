FROM python:3.9-alpine
WORKDIR /code
COPY pyproject.toml .
RUN addgroup -S appgroup && adduser --no-create-home -S appuser -G appgroup && \
    chown appuser:appgroup /code && \
    apk add --no-cache gcc musl-dev libffi-dev && \
    pip install --no-cache-dir poetry fastapi starlette_exporter redis uvicorn && \
    poetry install
COPY src src
USER appuser
CMD [ "uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "5000" ]
