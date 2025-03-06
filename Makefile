# ==============================================================================
# Base Variables
# ==============================================================================
PYTHON := python3.10
VENV := .venv
VENV_BIN := $(VENV)/bin
PROJECT_ROOT := $(shell pwd)
PYTHONPATH := $(PROJECT_ROOT)
LOCAL_TAG := $(shell date +"%Y-%m-%d-%H-%M")
LOCAL_IMAGE_NAME := stream-model-duration:$(LOCAL_TAG)
export PYTHONPATH

# Virtual environment executables
PIP := $(VENV_BIN)/pip
PYTHON_EXEC := $(VENV_BIN)/python
STREAMLIT_EXEC := $(VENV_BIN)/streamlit run

# Project directories
SRC_DIR := src
DOCS_DIR := docs
CHATBOT_PATH := $(SRC_DIR)/presentation/streamlit/app.py #$(SRC_DIR)/presentation/gradio/app.py

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
	@echo 'export PYTHONPATH="$${PYTHONPATH}:$(PROJECT_ROOT)"' >> $(VENV_BIN)/activate
	@echo "PYTHONPATH configuration complete"

# ==============================================================================
# Virtual Environment Setup
# ==============================================================================
.PHONY: check-python
check-python:
	@if ! command -v $(PYTHON) > /dev/null; then \
		echo "Python 3.10 not found. Installing..."; \
		sudo apt update && sudo apt install -y python3.10 python3.10-venv; \
	fi

$(VENV)/bin/activate:
	@if [ ! -d $(VENV) ]; then \
		echo "Creating virtual environment..."; \
		$(PYTHON) -m venv $(VENV); \
	fi
	@echo "Upgrading pip...";
	@$(PIP) install --upgrade pip

# ==============================================================================
# Setup and Installation
# ==============================================================================
.PHONY: setup
setup: check-python $(VENV)/bin/activate configure-pythonpath
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

.PHONY: install-dev
install-dev: setup
	$(PIP) install -e .

# ==============================================================================
# Running Applications
# ==============================================================================
.PHONY: run_app
run_chatbot_api: setup configure-pythonpath
	@echo "Starting chatbot API..."
	export PYTHONPATH=$(PYTHONPATH) && $(STREAMLIT_EXEC) $(CHATBOT_PATH)

# ==============================================================================
# Cleanup
# ==============================================================================
.PHONY: clean
clean:
	rm -rf $(VENV)
	rm -rf .pytest_cache .coverage htmlcov .mypy_cache **/__pycache__ **/*.pyc build/ dist/ *.egg-info

# ==============================================================================
# Help
# ==============================================================================
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make setup             : Set up development environment"
	@echo "  make clean             : Clean up generated files"
	@echo "  make run_chatbot_api   : Run the Chatbot API application"

.DEFAULT_GOAL := help