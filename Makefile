.PHONY: install test demo start dev clean help

# Python command
PYTHON := python3
PIP := pip3

# Default target
help:
	@echo "Call2Map - Available commands:"
	@echo ""
	@echo "  make install   - Install all dependencies"
	@echo "  make test      - Run all tests"
	@echo "  make demo      - Run demo test suite"
	@echo "  make start     - Start the FastAPI server"
	@echo "  make dev       - Start server with hot reload"
	@echo "  make clean     - Remove cache and temp files"
	@echo "  make help      - Show this help message"
	@echo ""

# Install dependencies
install:
	@echo "Installing dependencies..."
	$(PIP) install -r requirements.txt
	@echo "Installation complete!"

# Run all tests
test:
	@echo "Running installation tests..."
	@PYTHONPATH=. $(PYTHON) tests/test_installation.py
	@echo ""
	@echo "Running Gemini AI tests..."
	@PYTHONPATH=. $(PYTHON) tests/test_gemini.py
	@echo ""
	@echo "All tests passed!"

# Run demo test suite
demo:
	@echo "Running demo test suite..."
	@PYTHONPATH=. $(PYTHON) demo/demo_test.py
	@echo "Demo tests complete!"

# Start the server
start:
	@echo "Starting Call2Map server..."
	@echo "Server will be available at http://localhost:8000"
	$(PYTHON) main.py

# Start server with hot reload for development
dev:
	@echo "Starting server in development mode..."
	@echo "Hot reload enabled - server will restart on file changes"
	uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Clean cache files
clean:
	@echo "Cleaning cache and temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "Cleanup complete!"
