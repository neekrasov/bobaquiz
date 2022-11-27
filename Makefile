run:
	make -j 2 run-admin run-backend

run-admin:
	gunicorn src.app.admin:app --reload --bind 0.0.0.0:8001

run-backend:
	gunicorn src.app.app:app --reload --bind 0.0.0.0:8000 \
	--worker-class uvicorn.workers.UvicornWorker \
	--log-level debug \
	--workers $(WORKERS)

migrate-up:
	alembic upgrade head;

migrate-down:
	alembic downgrade $(revision);

migrate-create:
	alembic revision --autogenerate -m $(name);

migrate-history:
	alembic history;

migrate-stamp:
	alembic stamp -1;