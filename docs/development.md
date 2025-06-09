# Development Guide

This guide covers the development workflow, coding standards, and contributing to the Infoamazonia Boto project.

## Development Environment

### Local Development Setup

1. Follow the [installation instructions](installation.md) to set up your local environment.

2. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

3. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Code Structure

The project follows a modular structure:

```
src/
├── api/            # API endpoints and routes
├── core/           # Core application logic
├── db/             # Database models and connection
├── services/       # Business logic services
├── utils/          # Utility functions
└── main.py         # Application entry point
```

## Development Workflow

### 1. Branching Strategy

- `main` - Production-ready code
- `develop` - Development branch for integration
- Feature branches - For new features (`feature/feature-name`)
- Bug fix branches - For bug fixes (`fix/bug-description`)

### 2. Development Cycle

1. Create a new branch from `develop`
2. Implement your changes
3. Write/update tests
4. Run tests locally
5. Submit a Pull Request to `develop`

### 3. Testing

Run the test suite:

```bash
pytest
```

For coverage reports:

```bash
pytest --cov=src tests/
```

### 4. Code Quality

This project uses several tools to maintain code quality:

- **Black** for code formatting
- **Flake8** for linting
- **MyPy** for static type checking
- **isort** for import sorting

Run them all:

```bash
black src tests
flake8 src tests
mypy src
isort src tests
```

## Working with Docker

For a containerized development environment:

```bash
docker-compose -f docker-compose.dev.yml up
```

This will mount your local code as a volume, allowing you to make changes without rebuilding the container.

## Environment Variables

Key environment variables used in development:

- `DEBUG` - Enable debug mode (`True`/`False`)
- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - Secret key for security
- `LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)

## Documentation

### API Documentation

Update API documentation using OpenAPI specs. The application automatically generates Swagger UI at `/docs` when running.

### Project Documentation

This documentation is built with MkDocs:

1. Install MkDocs:
   ```bash
   pip install mkdocs mkdocs-material
   ```

2. Preview documentation:
   ```bash
   mkdocs serve
   ```

3. Build documentation:
   ```bash
   mkdocs build
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests for your changes
5. Ensure all tests pass
6. Submit a Pull Request

Please follow the project's coding standards and include appropriate tests.
