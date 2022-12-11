ifneq ($(wildcard deploy/.env),)
	ENV_FILE = .env
endif
ifneq ($(wildcard .env),)
	ifeq ($(DOCKER),)
		include .env
	endif
endif

export

run:
	make -j 2 run-admin run-backend

run-admin:
	poetry run gunicorn app.admin.main:app --reload --bind $(HOST):$(ADMIN_PORT)

run-backend:
	poetry run gunicorn app.api.main:app --reload --bind $(HOST):$(BACKEND_PORT) \
	--worker-class uvicorn.workers.UvicornWorker \
	--log-level ${LOG_LEVEL} \
	--workers $(WORKERS)

migrate-up:
	poetry run alembic -c ./deploy/alembic.ini upgrade head

migrate-down:
	poetry run alembic -c ./deploy/alembic.ini downgrade $(revision)

migrate-create:
	poetry run alembic -c ./deploy/alembic.ini revision --autogenerate -m $(name)

migrate-history:
	poetry run alembic -c ./deploy/alembic.ini history

migrate-stamp:
	poetry run alembic -c ./deploy/alembic.ini stamp $(revision)

compose-build:
	docker-compose -f ./deploy/docker-compose.yml --env-file deploy/$(ENV_FILE) build

compose-up:
	docker-compose -f ./deploy/docker-compose.yml --env-file deploy/$(ENV_FILE) up -d

compose-logs:
	docker-compose -f ./deploy/docker-compose.yml --env-file deploy/$(ENV_FILE) logs -f

compose-exec:
	docker-compose -f ./deploy/docker-compose.yml --env-file deploy/$(ENV_FILE) exec backend bash

docker-rm-volume:
	docker volume rm -f boba_db_data

compose-down:
	docker-compose -f ./deploy/docker-compose.yml --env-file deploy/$(ENV_FILE) down --remove-orphans