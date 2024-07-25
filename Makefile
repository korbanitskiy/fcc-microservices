SHELL = /bin/bash


.PHONY: format build up test

format:
	@ pre-commit run --all-files

build:
	@ docker compose pull --include-deps
	@ docker compose build

up:
	docker compose up --build

test:
	docker compose exec auth pytest 