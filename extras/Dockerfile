FROM ubuntu:18.04

MAINTAINER tfuntanilla "tfuntanilla@scu.edu"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY .. /app

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]

CMD [ "starter.py" ]