ifneq (,$(wildcard .env))
    include .env
    export
endif

run:
	make -j 2 run-admin run-backend

run-admin:
	poetry run gunicorn src.app.admin:app --reload --bind $(HOST):$(ADMIN_PORT)

run-backend:
	poetry run gunicorn src.app.app:app --reload --bind $(HOST):$(BACKEND_PORT) \
	--worker-class uvicorn.workers.UvicornWorker \
	--log-level ${LOG_LEVEL} \
	--workers $(WORKERS)

migrate-up:
	poetry run alembic upgrade head

migrate-down:
	poetry run alembic downgrade $(revision)

migrate-create:
	poetry run alembic revision --autogenerate -m $(name)

migrate-history:
	poetry run alembic history

migrate-stamp:
	poetry run alembic stamp $(revision)

compose-build:
	docker-compose -f docker/docker-compose.yml --env-file=.env build

compose-up:
	docker-compose -f docker/docker-compose.yml --env-file=.env up