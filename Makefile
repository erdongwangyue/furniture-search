.PHONY: install test lint format clean coverage setup-dev

# Development commands
install:
	pip install -r requirements.txt

setup-dev:
	pip install -e ".[dev]"

test:
	pytest -v

test-coverage:
	pytest --cov=app --cov-report=term-missing --cov-report=html

lint:
	flake8 app tests
	black --check app tests

format:
	black app tests
	isort app tests

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf furniture_search.egg-info
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

# Combined commands
setup: install setup-dev format lint test

# Development workflow
dev: format lint test 