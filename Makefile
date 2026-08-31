.PHONY: help venv install lint test smoke nc-ack preflight clean

PY ?= python3.12
VENV := .venv

help:
	@echo "Targets:"
	@echo "  venv       create local virtualenv"
	@echo "  install    install package + dev extras"
	@echo "  lint       ruff + bandit"
	@echo "  test       hermetic unit tests"
	@echo "  smoke      package-import smoke"
	@echo "  nc-ack     record the NC acknowledgement opt-in for this user"
	@echo "  preflight  verify NC acknowledgement is on file"

venv:
	$(PY) -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip

install: venv
	$(VENV)/bin/pip install -e .[dev,data]

lint:
	$(VENV)/bin/ruff check src tests scripts
	$(VENV)/bin/ruff format --check src tests scripts
	$(VENV)/bin/bandit -q -r src

test:
	$(VENV)/bin/pytest -m "not gpu and not integration" --cov=medimage_model_research

smoke:
	$(VENV)/bin/python -m medimage_model_research.cli smoke

nc-ack:
	$(VENV)/bin/python scripts/nc_acknowledge.py

preflight:
	$(VENV)/bin/python scripts/nc_acknowledge.py --check

clean:
	rm -rf $(VENV) build dist *.egg-info .pytest_cache .ruff_cache .coverage htmlcov
