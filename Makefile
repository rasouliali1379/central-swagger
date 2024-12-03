# Makefile for managing Swagger Aggregator project

# Backend variables
BACKEND_DIR = backend
BACKEND_REQUIREMENTS = requirements.txt
BACKEND_PORT = 8000
BACKEND_MAIN = app:app

# Frontend variables
FRONTEND_DIR = frontend
FRONTEND_PORT = 3000

.PHONY: install backend-install frontend-install start backend-start frontend-start stop backend-stop frontend-stop clean

install: backend-install frontend-install
	@echo "All dependencies installed."

backend-install:
	@echo "Installing backend dependencies..."
	pip install -r $(BACKEND_DIR)/$(BACKEND_REQUIREMENTS)

frontend-install:
	@echo "Installing frontend dependencies..."
	cd $(FRONTEND_DIR) && npm install

start: backend-start frontend-start
	@echo "Application started."

backend-start:
	@echo "Starting backend on port $(BACKEND_PORT)..."
	cd $(BACKEND_DIR) && uvicorn $(BACKEND_MAIN) --env-file .env --port $(BACKEND_PORT) &

frontend-start:
	@echo "Starting frontend on port $(FRONTEND_PORT)..."
	cd $(FRONTEND_DIR) && PORT=$(FRONTEND_PORT) npm start &

stop: backend-stop frontend-stop
	@echo "Application stopped."

backend-stop:
	@echo "Stopping backend on port $(BACKEND_PORT)..."
	@if lsof -i :$(BACKEND_PORT) -t > /dev/null 2>&1; then \
		kill -9 $$(lsof -i :$(BACKEND_PORT) -t); \
		echo "Backend stopped."; \
	else \
		echo "Backend is not running."; \
	fi

frontend-stop:
	@echo "Stopping frontend on port $(FRONTEND_PORT)..."
	@if lsof -i :$(FRONTEND_PORT) -t > /dev/null 2>&1; then \
		kill -9 $$(lsof -i :$(FRONTEND_PORT) -t); \
		echo "Frontend stopped."; \
	else \
		echo "Frontend is not running."; \
	fi

clean:
	@echo "Cleaning up temporary files..."
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	cd $(FRONTEND_DIR) && rm -rf node_modules
	cd $(BACKEND_DIR) && rm -rf __pycache__
	@echo "Cleanup complete."