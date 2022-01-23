FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

COPY ./requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

COPY ./yaml2rss/ /app/yaml2rss


ENV MODULE_NAME="yaml2rss.entrypoints.api.main"
ENV VARIABLE_NAME="api"
ENV WORKERS_PER_CORE=2
