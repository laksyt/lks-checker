FROM python:3.9-slim-buster

RUN adduser --system --group lks
USER lks:lks

WORKDIR /home/lks/app

RUN pip install pipenv

COPY Pipfile        Pipfile
COPY Pipfile.lock   Pipfile.lock

RUN /home/lks/.local/bin/pipenv install --deploy --ignore-pipfile

COPY main.py                            main.py
COPY laksyt/                            laksyt/
COPY profiles/                          profiles/
COPY ca.pem service.cert service.key    ./

ENV LAKSYT_PROFILE default

ENTRYPOINT ["/home/lks/.local/bin/pipenv", "run", "python", "main.py"]
