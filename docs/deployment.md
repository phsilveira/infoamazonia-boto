# Deployment to Azure

This guide explains how to deploy the Infoamazonia Boto application to Microsoft Azure.

## Prerequisites

- Azure subscription
- Azure CLI installed
- Azure Developer CLI (optional, for simplified deployment)
- Basic knowledge of Azure services

## First-time Setup

1. Install Azure CLI and log in:
   ```bash
   az login
   ```

2. Set your subscription:
   ```bash
   az account set --subscription <subscription-id>
   ```

3. Create required Azure resources using the bicep templates:
   ```bash
   cd infra
   az deployment group create --resource-group <resource-group-name> --template-file main.bicep --parameters main.parameters.json
   ```

## Deployment Options

### 1. Using Azure Developer CLI (Recommended)

The Azure Developer CLI (azd) provides a streamlined deployment experience:

1. Install Azure Developer CLI:
   ```bash
   curl -fsSL https://aka.ms/install-azd.sh | bash
   # Or on Windows: winget install Microsoft.Azd
   ```

2. Deploy the application:
   ```bash
   azd deploy
   ```

The command will guide you through the deployment process, including setting up required resources.

### 2. Manual Deployment

For more control over the deployment process:

1. Create a resource group (if not already created):
   ```bash
   az group create --name <resource-group-name> --location <location>
   ```

2. Deploy container registry:
   ```bash
   az acr create --resource-group <resource-group-name> --name <registry-name> --sku Basic
   ```

3. Build and push the Docker image:
   ```bash
   az acr build --registry <registry-name> --image infoamazonia-boto:latest .
   ```

4. Deploy Web App for Containers:
   ```bash
   az webapp create --resource-group <resource-group-name> --plan <app-service-plan> --name <app-name> --deployment-container-image-name <registry-name>.azurecr.io/infoamazonia-boto:latest
   ```

5. Configure environment variables:
   ```bash
   az webapp config appsettings set --resource-group <resource-group-name> --name <app-name> --settings @env-settings.json
   ```

## Infrastructure as Code

This project uses Azure Bicep for infrastructure definition. The templates are located in the `infra/` directory.

- `main.bicep` - Main infrastructure template
- `modules/` - Modular components for different Azure services
- `main.parameters.json` - Parameters for the deployment

## Monitoring and Maintenance

After deployment, monitor your application using:

- Azure Monitor
- Application Insights (if configured)
- Azure Log Analytics

For updates:

1. Make changes to your code
2. Build and push a new Docker image
3. Update the Web App to use the new image
