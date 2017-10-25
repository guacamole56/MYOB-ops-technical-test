# MYOB-ops-technical-test

[![Build Status](https://travis-ci.org/guacamole56/MYOB-ops-technical-test.svg?branch=master)](https://travis-ci.org/guacamole56/MYOB-ops-technical-test)

## General overview.

This is a very simple, stateless, dummy [Flask](http://flask.pocoo.org/) web
application that serves three HTTP endpoints per the [instructions provided](https://github.com/MYOB-Technology/ops-technical-test):

* `/` (root)
  * Main entrypoint to the app.
  * Returns a simple *"Hello World!"* message in plain text format.

* `/health`
  * Intended to be used as a lightweitght *ping* or healthcheck verification resource (used by, for
    example, load balancers) to assess the health of the web application.
  * Returns the string *"OK"* in plain text format.

* `/metadata`
  * Exposes general information about the application in JSON format.
  * Intended to be used by other (micro)services in the platform to gather
    details about the web application being served.
  * The pieces of information published are:
    - Name of the application.
    - Version.
    - Git unique identifier (an excerpt of the latest SHA commit id).
    - A brief description of the application's purpose.

All three endpoints support HTTP **GET** requests only.


## Testing.

A small suite of *unit tests* is provided under [myob_ops_technical_test/tests/](https://github.com/guacamole56/MYOB-ops-technical-test/tree/master/myob_ops_technical_test/tests) path.

[nose](http://nose.readthedocs.io/en/latest/) has been used during
  development to run the test suite and is used as well in the builds run by TravisCI. Other tools such as [pytest](https://docs.pytest.org/en/latest/) should work as well.

Also, a number of *smoke tests* are run at build time against the Docker
container image generated in TravisCI on each commit pushed to the *master*
branch in this GitHub repository.

These *smoke tests* are run via [pyresttest](https://github.com/svanoort/pyresttest), which provides a very simple and convenient way of testing any REST or Web API. See [docker/tests/web_smoketest.yaml](https://github.com/guacamole56/MYOB-ops-technical-test/blob/master/docker/tests/web_smoketest.yaml) for the list of tests of this type included.

## Packaging.

The Flask web application has been written as a python package that can be installed
using `pip` or `easy_install`. A [setup.py](https://github.com/guacamole56/MYOB-ops-technical-test/blob/master/setup.py) file with all the packaging-related
settings has been created for that purpose.

*Note*: The application has **only been tested with python 3.6.x**.

This package (**MYOB-Ops-Technical-Test**), along with all its required testing and execution dependencies, is automatically bundled on every successful build into a Docker image that is generated and later pushed against [guacamole56/myob-ops-technical-test](https://hub.docker.com/r/guacamole56/myob-ops-technical-test/tags/) DockerHub public repository.

## Building.

As mentioned above, a small CI pipeline has been set-up in TravisCI ([guacamole56 / MYOB-ops-technical-test](https://travis-ci.org/guacamole56/MYOB-ops-technical-test)) to automatically kick off the following action on each single commit:
1. Install the Flask web application plus all required dependencies.
1. Run the unit test suite.
1. Build a Docker image (see [Dockerfile](https://github.com/guacamole56/MYOB-ops-technical-test/blob/master/docker/Dockerfile) for more details) that runs the
   app.
1. Run a container of the aforementioned Docker image.
1. Run a small battery of *smoke* tests against that container.
1. If all steps above are successful the Docker image is tagged with the
   app's version and Git commit hash id and uploaded to DockerHub.

## Deployment.

### Install and run as a local Python package.

For development and local testing purposes, the app can be installed by running:
```
pip install -r requirements.txt
pip install .
```

*Optional.* Run tests (install `nose` via python *pip* if required):
```
nosetests
```
Run the app:
```
export FLASK_APP=myob_ops_technical_test
flask run
```
The app should be available at http://127.0.0.1:5000/ at this point.

### Deploy as Docker container image.

As explained in the *Building* section of this document, new Docker images are
built and uploaded to DockerHub on successful bulild completion in TravisCI.

The latest successful build is always available at `guacamole56/myob-ops-technical-test:latest` and each release is uniquely tagged. All of tham can be found [here](https://hub.docker.com/r/guacamole56/myob-ops-technical-test/tags/).

To run a Docker container with the latest version of the app execute:
```
docker run -d -p 5000:5000 guacamole56/myob-ops-technical-test:latest
```
The app will become available at http://127.0.0.1:5000/ in a few seconds.

## Future work.
These are multiple areas in which the application described here can be improved:
- Stop using Flask development web server and migrate to a more stable and high
  performance alternative such as [uwsgi](https://uwsgi-docs.readthedocs.io/en/latest/WSGIquickstart.html)
- Improve and extend the coverage of both unit and smoke tests.
- At the moment the web application logs are lost once the container is
  deleted. Ideally these should be saved or processed and their event sent,
  together with system metrics, to some centralized logging system for later analysis, such as [datadog](https://www.datadoghq.com/) or similar.
