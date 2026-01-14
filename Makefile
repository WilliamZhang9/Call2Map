.PHONY: install test start clean help

# Python command
PYTHON := python3
PIP := pip3

# Default target
help:
	@echo "Call2Map - Available commands:"
	@echo "  make install   - Install dependencies"
	@echo "  make test      - Run all tests"
	@echo "  make start     - Start the server"
	@echo "  make clean     - Remove cache files"
	@echo "  make help      - Show this help message"

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	$(PIP) install -r requirements.txt || true
	@echo "📦 Installing googlemaps from public PyPI..."
	$(PIP) install --index-url https://pypi.org/simple/ googlemaps>=4.10.0
	@echo "✅ Installation complete!"

# Run all tests
test:
	@echo "🧪 Running tests..."
	@PYTHONPATH=. $(PYTHON) tests/test_installation.py
	@echo ""
	@PYTHONPATH=. $(PYTHON) tests/test_gemini.py
	@echo "✅ All tests complete!"

# Start the server
start:
	@echo "🚀 Starting Call2Map server..."
	$(PYTHON) main.py

# Clean cache files
clean:
	@echo "🧹 Cleaning cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	@echo "✅ Cleanup complete!"
