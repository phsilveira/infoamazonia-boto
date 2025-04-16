# Installation Guide

This guide covers how to install and run the Infoamazonia Boto application using different methods.

## Prerequisites

- Python 3.9+
- Docker and Docker Compose (for containerized deployment)
- Git

## Local Installation

### 1. Clone the Repository

```bash
git clone https://github.com/infoamazonia/boto
cd infoamazonia-boto
```

### 2. Set Up a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
# For development dependencies:
pip install -r requirements-dev.txt
```

### 4. Configure Environment Variables

```bash
cp .env.sample .env
# Edit .env with your configuration
```

### 5. Run the Setup Script

```bash
./setup.sh
```

### 6. Start the Application

```bash
python src/main.py
```

The application should now be running at `http://localhost:8000`.

## Docker Installation

### Running with Docker Compose

1. Ensure Docker and Docker Compose are installed on your system.

2. Create environment variables:
   ```bash
   cp .env.sample .env
   # Edit .env with your configuration
   ```

3. Build and run the containers:
   ```bash
   docker-compose up --build
   ```

The application will be accessible at `http://localhost:8000` (or the port specified in your configuration).

## Development in Containers

### GitHub Codespaces / VSCode Dev Containers

This project supports development in containers via GitHub Codespaces or VSCode Dev Containers:

1. Open the project in VSCode
2. Click on the green button in the lower left corner and select "Reopen in Container"
3. Wait for the container to build and initialize
4. The development environment will be fully set up with all dependencies installed

## Troubleshooting

If you encounter issues during installation:

1. Ensure all prerequisites are correctly installed
2. Check that environment variables are properly configured
3. Verify network connections if the application needs to connect to external services
4. Consult the logs for specific error messages
