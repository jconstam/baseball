.PHONY: lint test

test: lint
	pytest

lint:
	flake8 . --ignore=E501 --statistics
