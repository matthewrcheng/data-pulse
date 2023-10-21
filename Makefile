# Makefile for Automated Data Analysis Tool

# Virtual Environment
VENV_NAME := .venv
PYTHON := $(VENV_NAME)/Scripts/python
PIP := $(VENV_NAME)/Scripts/pip

# Directories
SRC_DIR := src
TEST_DIR := tests

# Targets
.PHONY: install test coverage clean freeze

init:
	$(VENV_NAME)/bin/activate requirements.txt

install:
	@echo "Installing dependencies..."
	$(PIP) install -r requirements.txt

$(VENV_NAME)/bin/activate:
	@echo "Creating virtual environment..."
	python3 -m venv $(VENV_NAME)

test: install
	@echo "Running tests..."
	$(PYTHON) -m pytest $(TEST_DIR) --cov=$(SRC_DIR) --cov-report=term-missing

coverage: test
	@echo "Generating coverage report..."
	$(PYTHON) -m coverage html

clean:
	@echo "Cleaning up..."
	find . -name "*.pyc" -exec rm -f {} \;

freeze:
	@echo "Freezing dependencies..."
	$(PIP) freeze > requirements.txt