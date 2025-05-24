FROM python:3.13-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl python3-pip && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app/

RUN mkdir -p /app/logs

ENV PATH="/venv/bin:$PATH"

COPY app/pyproject.toml ./
COPY app/uv.lock* ./

RUN test -f uv.lock || uv lock && uv sync

copy app .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["uv", "run", "streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
