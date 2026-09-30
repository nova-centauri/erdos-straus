PYTHON ?= python3
export PYTHONPATH := .

.PHONY: check test verify-csv

check: test verify-csv

test:
	$(PYTHON) -m pytest

verify-csv:
	$(PYTHON) -m erdos_straus.cli check-csv data/triples.csv
	$(PYTHON) scripts/verify_triple.py --csv data/triples.csv
