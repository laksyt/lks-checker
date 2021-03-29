FROM python:3.9-slim-buster

RUN adduser --system --group lks
USER lks:lks

WORKDIR /home/lks/app

RUN pip install pipenv

COPY Pipfile        Pipfile
COPY Pipfile.lock   Pipfile.lock

RUN /home/lks/.local/bin/pipenv install --deploy --ignore-pipfile

COPY main.py        main.py
COPY laksyt/       checker/
COPY profiles/      profiles/

ENV LAKSYT_ENV prod

ENTRYPOINT ["/home/lks/.local/bin/pipenv", "run", "python", "main.py"]
