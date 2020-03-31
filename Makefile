.PHONY: update-deps
update-deps:
	pip install --upgrade pip-tools pip setuptools
	# pip-compile --upgrade --build-isolation --generate-hashes --output-file requirements/main.txt requirements/main.in
	# pip-compile --upgrade --build-isolation --generate-hashes --output-file requirements/dev.txt requirements/dev.in
	pip-compile --upgrade --build-isolation --output-file requirements/main.txt requirements/main.in
	pip-compile --upgrade --build-isolation --output-file requirements/dev.txt requirements/dev.in

.PHONY: init
init:
	pip install --editable .
	pip install --upgrade -r requirements/main.txt -r requirements/dev.txt
	rm -rf .tox
	pip install --upgrade tox
	pre-commit install

.PHONY: update
update: update-deps init

.PHONY: run
run:
	docker-compose up -d
	holdup -t 60 -T 5 -i 1 -n --insecure http://localhost:8081/subjects
	SAFIR_KAFKA_BROKER_URL=localhost:9092 SAFIR_SCHEMA_REGISTRY_URL=http://localhost:8081 adev runserver --app-factory create_app src/ltdevents/app.py

.PHONY: stop
stop:
	docker-compose down
