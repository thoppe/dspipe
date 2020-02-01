test:
	python -m pytest tests/

lint:
	black pipeline tests --line-length 80
