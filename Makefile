.PHONY: lint test coverage coveralls

coverage:
	coverage run --source=baseball --branch -m pytest tests/

coveralls: coverage
	coveralls --service=github

test:
	pytest

lint:
	flake8 . --ignore=E501 --statistics
