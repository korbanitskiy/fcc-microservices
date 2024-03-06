SHELL = /bin/bash


.PHONY: format build up

format:
	@ pre-commit run --all-files

build:
	@ docker compose pull --include-deps
	@ docker compose build

up:
	docker compose up
