.PHONY: lint test

coverage:
	coverage run --source=baseball --branch -m pytest tests/
	coveralls

test: lint
	pytest

lint:
	flake8 . --ignore=E501 --statistics
