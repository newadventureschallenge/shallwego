FROM python:3.13-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV PATH="/venv/bin:$PATH"

COPY . .

RUN test -f uv.lock || uv lock && uv sync

EXPOSE 8000

ENTRYPOINT ["uv", "run"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
