package_name=dspipe

test:
	python -m pytest tests/

coverage:
	coverage run --source=$(package_name) --omit $(package_name)/_version.py -m pytest tests/
	coverage report -m
	coverage html
	xdg-open htmlcov/index.html

lint:
	black $(package_name) tests --line-length 80

clean:
	rm -rvf htmlcov $(package_name).egg-info

dist_test:
	rm -rvf dist
	python setup.py sdist
	twine upload -r testpypi dist/* --verbose

dist_production:
	rm -rvf dist
	python setup.py sdist
	twine upload -r pypi dist/* --verbose
