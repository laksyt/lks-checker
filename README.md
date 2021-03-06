# Läksyt: Checker

<p align="center">
<em>‘Läksyt’ is plural for ‘homework’ in Finnish<br>(according to <a href="https://translate.google.com/?sl=fi&tl=en&text=l%C3%A4ksyt&op=translate">Google Translate</a>)</em>
</p>

A Python micro-service that periodically health-checks a list of websites, optionally searching for a regex pattern in
returned HTML, then sends the resulting health reports in Avro format to a Kafka topic.

## Configure

All configuration resides in the file `profiles/app-default.yml`.

The application looks for the `profiles` directory in the caller’s current working directory, then, if not found, in the application’s root directory (the one that contains `main.py`).

At the minimum, this application requires connection credentials to a Kafka instance, and a topic name to post to. Other
preferences are set to reasonable defaults and should prove intuitive to tinker with.

The application supports multiple configuration profiles: just add a file `profiles/app-<PROFILE_NAME>.yml` for each
additional profile.
(The profile `default` must always be present as it is, well, the default.)
To select the active profile:

* Set the environment variable `LAKSYT_PROFILE` to the value `<PROFILE_NAME>`.
* Or, add the command line option `--profile <PROFILE_NAME>`/`-p <PROFILE_NAME>` to the `python` command when launching
  the application.
* Otherwise, the `default` profile will be used.

The profile name given in the command line overrides the profile from the environment variable.

## Run

### Run with `pipenv`

To run the application with `pipenv`, first install the dependencies:

```shell
pipenv install --deploy --ignore-pipfile
```

Then run the application:

```shell
pipenv run python main.py
```

To select a non-default profile, append `-p <PROFILE_NAME>` to the `pipenv run` command.

### Run with Docker

To run the application with Docker, first build the image:

```shell
docker build -t laksyt/lks-checker:latest .
```

Then run the application:

```shell
docker run -it --rm laksyt/lks-checker:latest
```

To select a non-default profile, append `-e LAKSYT_PROFILE=<PROFILE_NAME>` to the `docker run` options.

## While running

The application logs its normal activities into the standard error at the `INFO` level. The lowest outputted log level
is controlled by the configuration key `log.level`.

To stop the execution, just send a `Ctrl-C`.
