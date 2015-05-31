.PHONY: all pep8 pyflakes clean test check docs

all:
	@echo 'pep8              check pep8 compliance'
	@echo 'pyflakes          check for unused imports (requires pyflakes)'
	@echo 'clean             cleanup the source tree'
	@echo 'test              run the unit tests'
	@echo 'check             make sure you are ready to commit'
	@echo 'docs              generate README.md from module docstring'

pep8:
	@pep8 backoff.py backoff_tests.py

pyflakes:
	@pyflakes backoff.py backoff_tests.py

clean:
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -delete

test: clean
	@PYTHONPATH=. py.test --cov-report term-missing --cov backoff.py backoff_tests.py

check: pep8 pyflakes test
	@coverage report | grep 100% >/dev/null || { echo 'Unit tests coverage is incomplete.'; exit 1; }

docs:
	@python -c 'import backoff ; print "# backoff" ; print "\n[![Build Status](https://travis-ci.org/litl/backoff.svg?branch=master)](https://travis-ci.org/litl/backoff?branch=master) [![Coverage Status](https://coveralls.io/repos/litl/backoff/badge.svg?branch=master)](https://coveralls.io/r/litl/backoff?branch=master)" ; print backoff.__doc__' > README.md
