# Makefile for Data Pulse

# Virtual Environment
VENV_NAME := venv
PYTHON := $(VENV_NAME)/Scripts/python
PIP := $(VENV_NAME)/Scripts/pip

# Backend Directories
BACKEND_DIR := backend
BACKEND_SRC_DIR := $(BACKEND_DIR)/src
BACKEND_TEST_DIR := $(BACKEND_DIR)/tests

# Frontend Directories
FRONTEND_DIR := frontend

# Targets
.PHONY: init-backend install-backend test-backend coverage-backend clean-backend freeze-backend \
        init-frontend install-frontend test-frontend build-frontend clean-frontend

init-backend: $(VENV_NAME)/Scripts/activate

install-backend: init-backend
	@echo "Installing backend dependencies..."
	@source $(VENV_NAME)/Scripts/activate && \
	$(PIP) install -r $(BACKEND_DIR)/requirements.txt

$(VENV_NAME)/Scripts/activate:
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV_NAME)

test-backend: install-backend
	@echo "Running backend tests..."
	$(PYTHON) -m pytest $(BACKEND_TEST_DIR) --cov=$(BACKEND_SRC_DIR) --cov-report=term-missing

coverage-backend: test-backend
	@echo "Generating backend coverage report..."
	$(PYTHON) -m coverage html -d $(BACKEND_DIR)/coverage

clean-backend:
	@echo "Cleaning up backend..."
	find $(BACKEND_DIR) -name "*.pyc" -exec rm -f {} \;
	rm -rf $(BACKEND_DIR)/coverage

start-backend:
	@echo "Starting backend server..."
	$(PYTHON) $(BACKEND_SRC_DIR)/main.py

freeze:
	@echo "Freezing backend dependencies..."
	$(PIP) freeze > $(BACKEND_DIR)/requirements.txt

init-frontend:
	@echo "Initializing frontend..."

install-frontend: init-frontend
	@echo "Installing frontend dependencies..."
	cd $(FRONTEND_DIR) && npm install

test-frontend: install-frontend
	@echo "Running frontend tests..."
	cd $(FRONTEND_DIR) && npm test

build-frontend: install-frontend
	@echo "Building frontend..."
	cd $(FRONTEND_DIR) && npm run build

clean-frontend:
	@echo "Cleaning up frontend..."
	cd $(FRONTEND_DIR) && npm run clean

start-frontend:
	@echo "Starting frontend server..."
	cd $(FRONTEND_DIR) && npm start

clean: clean-backend clean-frontend

test: test-backend test-frontend
