FROM python:alpine
LABEL maintainer="Patrick"
LABEL version="0.1"

RUN pip install requests

WORKDIR /app
ENTRYPOINT ["python"]
