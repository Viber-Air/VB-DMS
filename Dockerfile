FROM python:alpine

COPY requirements.txt ./
RUN  pip install --no-cache-dir -r requirements.txt
COPY api api

ENTRYPOINT sh ./api/run.sh
