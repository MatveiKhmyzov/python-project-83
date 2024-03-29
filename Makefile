install:
	poetry install
dev: 
	poetry run flask --app page_analyzer:app --debug run
PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
build:
	poetry build
package-install:
	python3 -m pip install dist/*.whl
package-reinstall:
	python3 -m pip install --force-reinstall dist/*.whl
lint:
	poetry run flake8 page_analyzer
    
.PHONY: install dev build package-install package-reinstall lint