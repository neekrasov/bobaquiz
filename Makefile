ifneq (,$(wildcard .env))
    include .env
    export
endif

run:
	make -j 2 run-admin run-backend

run-admin:
	poetry run gunicorn app.admin.main:app \
	--reload --bind $(HOST):$(ADMIN_PORT) \
	--worker-class gevent 

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
	docker-compose -f ./deploy/docker-compose.yml --env-file deploy/.env build

compose-up:
	docker-compose -f ./deploy/docker-compose.yml --env-file deploy/.env up -d

compose-logs:
	docker-compose -f ./deploy/docker-compose.yml --env-file deploy/.env logs -f

compose-exec:
	docker-compose -f ./deploy/docker-compose.yml --env-file deploy/.env exec backend bash

docker-rm-volume:
	docker volume rm -f boba_db_data

compose-down:
	docker-compose -f ./deploy/docker-compose.yml --env-file deploy/.env down --remove-orphans