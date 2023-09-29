SHELL = /bin/bash

.PHONY: setup
setup: create-admin-api-token build create-db migrate-db upload-sitemap start import-datamarts wait import-configs
	@ echo "[setup]: DONE"
	@ echo "[setup]: Go to https://mss.local/rgmx-lsm"
	@ echo "[setup]: Log in with static-passwords = admin@example.com:password"


.PHONY: build
build:
	@ docker-compose pull --include-deps
	@ docker-compose build


.PHONY: start
start:
	@ echo "[start]: starting docker containers..."
	@ docker-compose up -d --force-recreate
	@ echo "[start]: DONE"

.PHONY: stop
stop: ## Stops all services
	@ echo "[stop]: stopping docker containers..."
	@ docker-compose stop
	@ echo "[stop]: DONE"


.PHONY: format
format: 
	@ ruff --fix src/
