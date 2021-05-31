.PHONY: lint test

coverage_github:
	coverage run --source=baseball --service=github --branch -m pytest tests/
	coveralls

coverage:
	coverage run --source=baseball --branch -m pytest tests/
	coveralls

test: lint
	pytest

lint:
	flake8 . --ignore=E501 --statistics
