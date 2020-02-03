package_name=dspipe

test:
	python -m pytest tests/

coverage:
	coverage run --source=$(package_name) -m pytest tests/
	coverage report -m
	coverage html
	xdg-open htmlcov/index.html

lint:
	black $(package_name) tests --line-length 80

clean:
	rm -rvf htmlcov $(package_name).egg-info
