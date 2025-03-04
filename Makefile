# ==============================================================================
# Base Variables
# ==============================================================================
PYTHON := python3.10
VENV := .venv
VENV_BIN := $(VENV)/bin
PROJECT_ROOT := $(shell pwd)
PYTHONPATH := $(PROJECT_ROOT)/src:$(PYTHONPATH)
LOCAL_TAG := $(shell date +"%Y-%m-%d-%H-%M")
LOCAL_IMAGE_NAME := stream-model-duration:${LOCAL_TAG}
export PYTHONPATH

# Virtual environment executables
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest
COVERAGE := $(VENV)/bin/coverage
FLAKE8 := $(VENV)/bin/flake8
BLACK := $(VENV)/bin/black
ISORT := $(VENV)/bin/isort
MYPY := $(VENV)/bin/mypy

# Project directories
SRC_DIR := src
TEST_DIR := tests
DOCS_DIR := docs
DATA_FETCHER_PATH := src/multiAgent/app/main.py
CHATBOT_PATH := src/multiAgent/presentation/api/main.py
GRAPH_EVAL_PATH := src/multiAgent/eval/run_eval.py

# Environment configuration
SHELL := /bin/bash
ENV_FILE := .env

# Debug configuration
DEBUG ?= 0
ifeq ($(DEBUG),1)
    MAKEFLAGS += --warn-undefined-variables
    .SHELLFLAGS := -xec
endif

# ==============================================================================
# Python Path Configuration
# ==============================================================================
.PHONY: configure-pythonpath
configure-pythonpath: $(VENV)/bin/activate
	@echo "Configuring PYTHONPATH in virtual environment..."
	@# For bash activation script
	@echo 'export PYTHONPATH="$(PROJECT_ROOT)/src:$$PYTHONPATH"' >> $(VENV)/bin/activate
	@# For fish activation script (if you use fish shell)
	@if [ -f "$(VENV)/bin/activate.fish" ]; then \
		echo 'set -x PYTHONPATH "$(PROJECT_ROOT)/src:$$PYTHONPATH"' >> $(VENV)/bin/activate.fish; \
	fi
	@# For csh/tcsh activation script
	@if [ -f "$(VENV)/bin/activate.csh" ]; then \
		echo 'setenv PYTHONPATH "$(PROJECT_ROOT)/src:$$PYTHONPATH"' >> $(VENV)/bin/activate.csh; \
	fi
	@echo "PYTHONPATH configuration complete"

# ==============================================================================
# Environment Variable Handling Functions
# ==============================================================================
define load_env_vars
	@echo "Debug: Current shell is $$SHELL"
	@echo "Debug: Attempting to load $(ENV_FILE)"
	@if [ ! -f "$(ENV_FILE)" ]; then \
		echo "Error: $(ENV_FILE) does not exist"; \
		exit 1; \
	fi
	@if [ ! -r "$(ENV_FILE)" ]; then \
		echo "Error: $(ENV_FILE) is not readable"; \
		exit 1; \
	fi
	$(eval $(shell sed 's/=.*$$//g; s/^/export /g' ${ENV_FILE}))
	@echo "Debug: Environment file processed"
endef

define check_openai_key
	@echo "Checking OPENAI_API_KEY..."
	@if [ -f "$(ENV_FILE)" ]; then \
		if grep -q "^OPENAI_API_KEY=" "$(ENV_FILE)"; then \
			echo "OPENAI_API_KEY found in $(ENV_FILE)"; \
			. $(ENV_FILE); \
			if [ -n "$OPENAI_API_KEY" ]; then \
				echo "OPENAI_API_KEY successfully loaded."; \
			else \
				echo "Error: OPENAI_API_KEY is empty in $(ENV_FILE)"; \
				exit 1; \
			fi; \
		else \
			echo "Error: OPENAI_API_KEY not found in $(ENV_FILE)"; \
			echo "Content of $(ENV_FILE):"; \
			cat $(ENV_FILE) | grep -v "SECRET\|KEY\|PASS" || true; \
			exit 1; \
		fi; \
	else \
		echo "Error: $(ENV_FILE) file not found."; \
		exit 1; \
	fi
endef

# ==============================================================================
# Docker and Docker Compose Commands
# ==============================================================================
.PHONY: docker-build
docker-build: quality_checks test
	docker build -t ${LOCAL_IMAGE_NAME} .

.PHONY: docker-compose-up
docker-compose-up:
	docker-compose up -d

.PHONY: docker-compose-down
docker-compose-down:
	docker-compose down

.PHONY: docker-compose-logs
docker-compose-logs:
	docker-compose logs -f

# ==============================================================================
# Development Environment Setup
# ==============================================================================
.PHONY: check-python
check-python:
	@if ! command -v $(PYTHON) > /dev/null; then \
		echo "Python 3.10 not found. Installing..."; \
		sudo apt update && sudo apt install -y software-properties-common && \
		sudo add-apt-repository -y ppa:deadsnakes/ppa && sudo apt update && \
		sudo apt install -y python3.10 python3.10-venv; \
	fi

$(VENV)/bin/activate:
	@if [ ! -d $(VENV) ]; then \
		echo "Creating virtual environment..."; \
		$(PYTHON) -m venv $(VENV) || { \
			echo "Error: Failed to create virtual environment. Trying to fix dependencies..."; \
			sudo apt update && sudo apt install -y python3.10-venv || { \
				echo "Error: Unable to fix dependencies. Please check your Python installation."; \
				exit 1; \
			}; \
			$(PYTHON) -m venv $(VENV) || { \
				echo "Error: Virtual environment creation failed even after fixing dependencies."; \
				exit 1; \
			}; \
		}; \
	fi
	@echo "Upgrading pip...";
	@$(VENV)/bin/pip install --upgrade pip || { \
		echo "Error: Failed to upgrade pip. Please check your virtual environment setup."; \
		exit 1; \
	}

# ==============================================================================
# Testing and Quality Checks
# ==============================================================================
.PHONY: test
test: setup
	$(call load_env_vars)
	$(call check_openai_key)
	. $(ENV_FILE) && $(PYTEST) $(TEST_DIR) -v

.PHONY: coverage
coverage: setup
	$(call load_env_vars)
	$(call check_openai_key)
	$(COVERAGE) run -m pytest $(TEST_DIR)
	$(COVERAGE) report -m
	$(COVERAGE) html

.PHONY: quality_checks
quality_checks:
	@echo "Automatically fixing code style issues..."
	@if ! $(BLACK) --config pyproject.toml $(SRC_DIR) $(TEST_DIR); then \
		echo "Warning: Black formatting failed, continuing with other checks..."; \
	fi
	@if ! $(ISORT) --settings-path pyproject.toml $(SRC_DIR) $(TEST_DIR); then \
		echo "Warning: isort failed, continuing with other checks..."; \
	fi
	@echo "Running code quality checks..."
	@if command -v flake8-pyproject >/dev/null 2>&1; then \
		$(FLAKE8) --config=pyproject.toml $(SRC_DIR) $(TEST_DIR); \
	else \
		$(FLAKE8) --config=.flake8 $(SRC_DIR) $(TEST_DIR); \
	fi
	@if ! $(MYPY) --config-file pyproject.toml $(SRC_DIR); then \
		echo "Warning: mypy type checking failed, please review the errors."; \
	fi

.PHONY: integration_test
integration_test: docker-build
	LOCAL_IMAGE_NAME=${LOCAL_IMAGE_NAME} bash integration-test/run.sh

# ==============================================================================
# Code Quality Tools
# ==============================================================================
.PHONY: lint
lint: flake8 black-check isort-check mypy

.PHONY: flake8
flake8:
	$(FLAKE8) --config=.flake8 $(SRC_DIR) $(TEST_DIR)

.PHONY: black
black:
	$(BLACK) --config pyproject.toml $(SRC_DIR) $(TEST_DIR)

.PHONY: black-check
black-check:
	$(BLACK) --config pyproject.toml --check $(SRC_DIR) $(TEST_DIR)

.PHONY: isort
isort:
	$(ISORT) --settings-path pyproject.toml --diff --verbose $(SRC_DIR) $(TEST_DIR)

.PHONY: isort-check
isort-check:
	$(ISORT) --settings-path pyproject.toml --check-only --diff $(SRC_DIR) $(TEST_DIR)

.PHONY: mypy
mypy:
	$(MYPY) --config-file pyproject.toml $(SRC_DIR)

# ==============================================================================
# Application Commands
# ==============================================================================
.PHONY: run_graph_evaluation
run_graph_evaluation: setup
	$(call load_env_vars)
	$(call check_openai_key)
	$(VENV)/bin/python $(GRAPH_EVAL_PATH)
	
.PHONY: run_chatbot_api
run_chatbot_api: setup
	@echo "Starting chatbot API..."
	$(call load_env_vars)
	$(call check_openai_key)
	$(VENV)/bin/python $(CHATBOT_PATH)

.PHONY: run_data_fetcher
run_data_fetcher: setup
	$(call load_env_vars)
	$(call check_openai_key)
	$(VENV)/bin/python $(DATA_FETCHER_PATH)

# ==============================================================================
# Setup and Installation
# ==============================================================================
.PHONY: setup
setup: $(VENV)/bin/activate configure-pythonpath
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install -r requirements-dev.txt

.PHONY: install-dev
install-dev: setup
	$(PIP) install -e .

.PHONY: pre-commit
pre-commit: setup
	$(PIP) install pre-commit
	pre-commit install

# ==============================================================================
# Cleanup and Build
# ==============================================================================
.PHONY: clean
clean:
	rm -rf $(VENV)
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf .mypy_cache
	rm -rf **/__pycache__
	rm -rf **/*.pyc
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

.PHONY: build
build: quality_checks test docker-build

.PHONY: publish
publish: build integration_test
	LOCAL_IMAGE_NAME=${LOCAL_IMAGE_NAME} bash scripts/publish.sh

# ==============================================================================
# Help
# ==============================================================================
.PHONY: help
help:
	@echo "Available commands:"
	@echo "Development:"
	@echo "  make setup             : Set up development environment"
	@echo "  make clean             : Clean up generated files"
	@echo "  make install-dev       : Install package in development mode"
	@echo "  make pre-commit        : Install pre-commit hooks"
	@echo ""
	@echo "Testing:"
	@echo "  make test              : Run tests"
	@echo "  make coverage          : Run tests with coverage report"
	@echo "  make integration_test  : Run integration tests"
	@echo ""
	@echo "Code Quality:"
	@echo "  make quality_checks    : Run all code quality checks"
	@echo "  make lint              : Run all linting checks"
	@echo "  make format            : Format code with black and isort"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build      : Build Docker image"
	@echo "  make docker-compose-up : Start services with docker-compose"
	@echo "  make docker-compose-down: Stop services"
	@echo ""
	@echo "Applications:"
	@echo "  make run_chatbot_api   : Run the Chatbot API application"

.DEFAULT_GOAL := help