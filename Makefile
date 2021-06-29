run-dev:
	PYTHONUNBUFFERED=1 HOST=127.0.0.1 HOST_PORT=5000 FLASK_ENV=development FLASK_CONFIG_DEFAULT=Dev \
	venv/bin/gunicorn wsgi:app --worker-class eventlet -w 1 -b 127.0.0.1:5000 -t 600 --reload \
	--reload-extra-file templates/base.html \
	--reload-extra-file templates/upload.html \
	--reload-extra-file templates/result.html 

# runs all tests
test:
	HOST=dv.local HOST_PORT=5000 FLASK_ENV=development FLASK_CONFIG_DEFAULT=Test pytest

# flask-migrate commands shortcuts
db-init:
	FLASK_ENV=development FLASK_CONFIG_DEFAULT=Dev flask db init

db-migrate:
	FLASK_ENV=development FLASK_CONFIG_DEFAULT=Dev flask db migrate -m '$(msg)'

db-upgrade:
	FLASK_ENV=development FLASK_CONFIG_DEFAULT=Dev flask db upgrade $(rev)

db-downgrade:
	FLASK_ENV=development FLASK_CONFIG_DEFAULT=Dev flask db upgrade $(rev)

db-history:
	FLASK_ENV=development FLASK_CONFIG_DEFAULT=Dev flask db history

db-current:
	FLASK_ENV=development FLASK_CONFIG_DEFAULT=Dev flask db current
