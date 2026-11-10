PY ?= .venv/bin/python

.PHONY: check test reproduce flash-campaign flash-verify

check:
	$(PY) scripts/check.py

test:
	$(PY) -m pytest -q tests

# Regenerate every results table offline from logged runs.
reproduce:
	$(PY) -m flash_demo.analysis

flash-campaign:
	$(PY) -m flash_demo.campaign

flash-verify:
	$(PY) -m flash_demo.verify
