.PHONY: test black isort mypy

CMD:=poetry run

test:
				$(CMD) pytest -vv --cov=htm2md

black:
				$(CMD) black htm2md

isort:
				$(CMD) isort htm2md

mypy:
				$(CMD) mypy htm2md
