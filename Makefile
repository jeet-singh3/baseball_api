.PHONY: all prepare-dev denv lint test run shell clean build install docker
SHELL=/bin/bash

VENV_NAME?=venv
VENV_BIN=$(shell pwd)/${VENV_NAME}/bin
python=${VENV_BIN}/python3
FLASK=${VENV_BIN}/flask

export FLASK_ENV=development
export FLASK_APP=

all:
	@echo "make run		-	Run the REST API server"
	@echo "make test	-	Run tests on the project"
	@echo "make init	-	Create python virtual environment and install dependencies"
	@echo "make docker	-	Run the REST API server in a dockerized container"

test:
	docker-compose down
	docker build -t baseballapi .
	docker-compose run --entrypoint "/app/test.sh" api
	docker-compose down

test-inside-docker:
	sleep 5
	pytest --disable-pytest-warnings --cov=app

db-up:
	docker-compose down
	docker-compose up -d postgres

db-down:
	docker-compose down

docker:
	docker-compose down
	docker-compose up --build --force-recreate

base:
	docker login
	docker build --file ./Dockerfile.base -t jeeter30/flaskapi_api:base .
	docker push jeeter30/flaskapi_api:base
