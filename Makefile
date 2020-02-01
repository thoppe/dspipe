test:
	python -m pytest tests/

coverage:
	coverage run --source=pipeline -m pytest tests/
	coverage report -m
	coverage html
	xdg-open htmlcov/index.html

lint:
	black pipeline tests --line-length 80

clean:
	rm -rvf cover
