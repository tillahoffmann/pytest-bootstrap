.PHONY : docs doctest lint sdist sync tests

build : lint tests docs doctest sdist

lint :
	flake8 --exclude=docs/_build

tests :
	pytest -v --cov=pytest_bootstrap --cov-fail-under=100 --cov-report=term-missing --cov-report=html

docs :
	rm -rf docs/_build/plot_directive
	sphinx-build . docs/_build

doctest :
	sphinx-build -b doctest . docs/_build

sync : requirements.txt
	pip-sync

requirements.txt : requirements.in setup.py test_requirements.txt
	pip-compile -v --upgrade -o $@ $<

test_requirements.txt : test_requirements.in setup.py
	pip-compile -v --upgrade -o $@ $<

VERSION :
	python generate_version.py

sdist : VERSION
	python setup.py sdist
	twine check dist/*.tar.gz
