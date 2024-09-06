VENV_DIR=venv

PYTHON=$(VENV_DIR)/bin/python

PIP=$(VENV_DIR)/bin/pip

FLASK=$(VENV_DIR)/bin/flask

PYTEST=$(VENV_DIR)/bin/pytest

$(VENV_DIR)/bin/activate: requirements.txt
	@echo "Creating virtual environment..."
	@python3 -m venv $(VENV_DIR)
	@echo "Installing dependencies..."
	@$(PIP) install -r requirements.txt

flask-dev: $(VENV_DIR)/bin/activate
	@echo "Starting Flask development server..."
	@chmod +x ./init-mongodb.sh
	@./init-mongodb.sh
	ENV_FOR_DYNACONF=development $(FLASK) run

pytest: $(VENV_DIR)/bin/activate
	@$(PYTEST) --cov=application --cov-report=term-missing --cov-fail-under=74

pytest-cov: $(VENV_DIR)/bin/activate
	@$(PYTEST) --cov=application --cov-report=html --cov-fail-under=74

clear:
	@echo "Cleaning up..."
	@rm -rf .pytest_cache
	@rm -rf htmlcov
	@rm -rf $(VENV_DIR)

.PHONY: flask-dev pytest pytest-cov clean

save-dependencies:
	@$(PIP) freeze > requirements.txt

