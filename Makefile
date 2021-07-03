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

$(VENV_NAME)/bin/activate: requirements.txt
	make pip
	touch $(VENV_NAME)/bin/activate

test:
	docker-compose down
	docker build -t baseballapi .
	docker-compose run --entrypoint "/app/test.sh" api
	docker-compose down

test-inside-docker:
	sleep 5
	pytest --disable-pytest-warnings --cov=app

pip:
	test -d $(VENV_NAME) || virtualenv -p python3 $(VENV_NAME)
	source $(VENV_NAME)/bin/activate
	${PYTHON} -m pip install -r requirements.txt

db-up:
	docker-compose down
	docker-compose up -d postgres

db-down:
	docker-compose down

run:
	${FLASK} run --port=5000 2>&1

docker:
	docker system prune
	docker-compose up --build --force-recreate

base:
	docker login
	docker build --file ./Dockerfile.base -t jeeter30/flaskapi_api:base .
	docker push jeeter30/flaskapi_api:base
