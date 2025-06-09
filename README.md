# Infoamazonia Boto

## Table of Contents
- Overview
- Prerequisites
- Local Development
- Docker Development
- Deployment to Azure
- Environment Variables
- License

## Overview
This repository contains the Infoamazonia Boto application, a Python-based web application deployable to Azure.

## Prerequisites
- Python 3.9+
- Docker and Docker Compose
- Azure CLI
- Azure subscription (for deployment)
- Git

## Local Development

### Setup
1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd infoamazonia-boto
   ```

2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   # For development dependencies:
   pip install -r requirements-dev.txt
   ```

4. Set up environment variables:
   ```sh
   cp .env.sample .env
   # Edit .env with your configuration
   ```

5. Run the setup script:
   ```sh
   ./setup.sh
   ```

6. Run the application:
   ```sh
   python src/main.py
   ```

## Docker Development

### Running with Docker Compose
1. Make sure Docker and Docker Compose are installed on your system.

2. Create environment variables:
   ```sh
   cp .env.sample .env
   # Edit .env with your configuration
   ```

3. Build and run the containers:
   ```sh
   docker-compose up --build
   ```

4. Access the application at `http://localhost:8000` (or the port specified in your configuration).

### GitHub Codespaces / VSCode Dev Containers
This project supports development in containers via GitHub Codespaces or VSCode Dev Containers:

1. Open the project in VSCode
2. Click on the green button in the lower left corner and select "Reopen in Container"
3. Wait for the container to build and initialize
4. The development environment will be fully set up with all dependencies installed

## Deployment to Azure

### First-time Setup
1. Install Azure CLI and log in:
   ```sh
   az login
   ```

2. Set your subscription:
   ```sh
   az account set --subscription <subscription-id>
   ```

3. Create required Azure resources using the bicep templates:
   ```sh
   cd infra
   az deployment group create --resource-group <resource-group-name> --template-file main.bicep --parameters main.parameters.json
   ```

### Deployment using Azure Developer CLI
1. Make sure you have Azure Developer CLI installed:
   ```sh
   curl -fsSL https://aka.ms/install-azd.sh | bash
   # Or on Windows: winget install Microsoft.Azd
   ```

2. Deploy the application:
   ```sh
   azd deploy
   ```

### Manual Deployment
1. Build the Docker image:
   ```sh
   docker build -t infoamazonia-boto .
   ```

2. Tag and push to Azure Container Registry:
   ```sh
   az acr login --name <your-acr-name>
   docker tag infoamazonia-boto <your-acr-name>.azurecr.io/infoamazonia-boto:latest
   docker push <your-acr-name>.azurecr.io/infoamazonia-boto:latest
   ```

3. Deploy to Azure App Service:
   ```sh
   az webapp config container set --name <app-name> --resource-group <resource-group> --docker-custom-image-name <your-acr-name>.azurecr.io/infoamazonia-boto:latest
   ```

## Environment Variables
The application uses the following environment variables (see .env.sample for reference):

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:postgres@localhost:5432/boto` |
| `SECRET_KEY` | Secret key for security | `your-secret-key` |
| `DEBUG` | Enable debug mode | `True` |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | `localhost,127.0.0.1` |
| ... | ... | ... |

## License
See LICENSE file for details.