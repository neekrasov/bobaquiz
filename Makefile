run:
	make -j 2 run-admin run-backend

run-admin:
	gunicorn src.app.admin:app --reload --bind 0.0.0.0:8001

run-backend:
	gunicorn src.app.app:app --reload --bind 0.0.0.0:8000 \
	--worker-class uvicorn.workers.UvicornWorker \
	--workers $(WORKERS)

migrate-up:
	cd src/db && alembic upgrade head;

migrate-down:
	cd src/db && alembic downgrade $(revision);

migrate-create:
	cd src/db && alembic revision --autogenerate -m $(name);