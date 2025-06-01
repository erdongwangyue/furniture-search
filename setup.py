from setuptools import setup, find_packages

setup(
    name="furniture-search",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "azure-search-documents>=11.4.0",
        "azure-identity==1.15.0",
        "python-dotenv==1.0.0",
        "fastapi==0.115.12",
        "uvicorn==0.24.0",
        "pydantic==2.11.5",
        "pydantic-settings>=2.4.0",
        "structlog==23.2.0",
        "python-json-logger==2.0.7",
    ],
    extras_require={
        "dev": [
            "pytest==7.4.3",
            "pytest-cov==4.1.0",
            "pytest-asyncio==0.21.1",
            "httpx==0.25.1",
            "black==23.11.0",
            "isort==5.12.0",
            "flake8==6.1.0",
        ],
    },
) 