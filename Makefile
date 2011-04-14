all:
	@echo "Nothing to do"

sdist:
	@pandoc README.md -t rst > README.rst
	python setup.py sdist

