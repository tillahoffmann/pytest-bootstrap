.PHONY : docs lint sync tests

build : lint tests docs

lint :
	flake8

tests :
	pytest -v --cov=pytest_bootstrap --cov-fail-under=100 --cov-report=term-missing --cov-report=html

docs :
	sphinx-build . docs/_build

sync : requirements.txt
	pip-sync

requirements.txt : requirements.in setup.py test_requirements.txt
	pip-compile -v --upgrade -o $@ $<

test_requirements.txt : test_requirements.in setup.py
	pip-compile -v --upgrade -o $@ $<
