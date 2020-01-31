test:
	python -m pytest --workers auto --durations=5 tests/

lint:
	black pipeline tests --line-length 80
