.PHONY: lint test

coverage:
	coverage run --source=baseball --branch -m pytest tests/

coveralls: coverage
	coveralls --service=github

test: lint
	pytest

lint:
	flake8 . --ignore=E501 --statistics
