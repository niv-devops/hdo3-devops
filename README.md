# DevOps Pro Pipeline Project

This repository is a comprehensive example of a **Full DevOps Pipeline** that integrates a wide range of tools and technologies used in modern DevOps workflows. The pipeline includes **GitLab**, **Docker**, **Jenkins**, **Kubernetes (K8s)**, **Ansible**, **Python**, **JavaScript**, **MongoDB**, **Slack**, **Goofy**, **Prometheus**, **Grafana**, **Helm**, **ArgoCD**, **SonarQube**, **Hadolint**, **HashiCorp Vault**, and **Nexus Registry**.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Setup Instructions](#setup-instructions)
4. [Pipeline Workflow](#pipeline-workflow)
5. [Slack Notifications](#slack-notifications)
6. [Monitoring and Alerts](#monitoring-and-alerts)
7. [Infrastructure as Code](#infrastructure-as-code)
8. [Security and Secrets Management](#security-and-secrets-management)
9. [CI/CD Details](#cicd-details)
10. [Deployment](#deployment)
11. [License](#license)

## Project Overview

This project demonstrates the use of several tools in the DevOps ecosystem to automate the entire application lifecycle, from code commit to deployment in production. The pipeline automates tasks such as:

- **Code Quality Analysis**
- **Build & Test Automation**
- **Containerization & Image Management**
- **Infrastructure Automation**
- **Continuous Integration & Continuous Delivery (CI/CD)**
- **Cluster Deployment with Slack Notification**
- **Monitoring and Logging**

## Technology Stack

The following tools are integrated into the pipeline:

- **GitLab**: Version control and repository management.
- **Docker**: Containerization and image creation.
- **Jenkins**: Automation server to run the CI/CD pipeline.
- **Kubernetes (K8s)**: Container orchestration for deploying and managing containers.
- **Ansible**: Configuration management and automation tool.
- **Python**: Backend application development.
- **JavaScript**: Frontend application development.
- **MongoDB**: NoSQL database for backend storage.
- **Slack**: Notifications for build and deployment status.
- **Prometheus**: Monitoring tool for metrics collection.
- **Grafana**: Visualization tool for Prometheus metrics.
- **Helm**: Kubernetes package manager for deploying applications.
- **ArgoCD**: Continuous delivery tool for Kubernetes deployments.
- **SonarQube**: Code quality analysis and static code analysis.
- **Hadolint**: Linter for Dockerfiles.
- **HashiCorp Vault**: Secret management for secure storage of credentials.
- **Nexus Registry**: Artifact registry for managing Docker images.

## Setup Instructions

### Prerequisites

- **Docker**: Ensure Docker is installed and running on your machine.
- **Kubernetes Cluster**: A running Kubernetes cluster for deployments (can be a local or cloud-based setup).
- **Jenkins**: Set up Jenkins for pipeline execution.
- **GitLab**: GitLab for version control and source code repository.
- **Prometheus and Grafana**: Setup Prometheus and Grafana for monitoring.
- **SonarQube**: Set up SonarQube for code quality analysis.
- **Slack**: Create a Slack channel for notifications.
- **HashiCorp Vault**: Set up HashiCorp Vault for secret management.
- **Nexus Registry**: Set up Nexus as a Docker registry for image storage.

### Clone the Repository

```bash
git clone http://10.4.0.19:9090/hdo3/goofy.git
cd goofy
```

### Jenkins Setup

- Install Jenkins with necessary plugins such as **Docker**, **Kubernetes**, **GitLab**, **SonarQube**, and **Slack Notification**.
- Create credentials for Docker and GitLab inside Jenkins.

### Kubernetes Setup

- Install Helm and configure ArgoCD for Kubernetes-based deployment.
- Configure `kubectl` to connect to your Kubernetes cluster.

### SonarQube and Hadolint Setup

- Install and configure SonarQube for code quality analysis.
- Install Hadolint for Dockerfile linting during the build process.

## Pipeline Workflow

The pipeline workflow follows these stages:

### 1. **SCM (Source Code Management)**

- The code is pulled from the GitLab repository to the Jenkins workspace for further processing.

### 2. **Install Dependencies**

- The required dependencies for Python are installed using `pip`.

### 3. **SonarQube Analysis**

- SonarQube performs static code analysis on both Python and JavaScript code to ensure quality and adherence to coding standards.

### 4. **Hadolint Dockerfile**

- Hadolint is used to lint the Dockerfile for best practices and security vulnerabilities.

### 5. **Build Docker Image**

- The application is containerized using Docker, and the image is built using the `docker.build()` command in Jenkins.

### 6. **Push Docker Image to Nexus Registry**

- The Docker image is tagged with the build number and pushed to the Nexus registry for storage and later use in deployments.

### 7. **Deploy to Kubernetes**

- The Docker image is deployed to Kubernetes using **Helm** charts and **ArgoCD** for continuous delivery.

## Slack Notifications

The pipeline sends notifications to Slack for the following events:

- **Build Success**: A notification is sent when the build and tests pass successfully.
- **Build Failure**: A notification is sent when the build or tests fail.

You can customize the Slack integration by configuring the Slack Webhook URL in Jenkins.

## Monitoring and Alerts

- **Prometheus**: Monitors application and infrastructure metrics.
- **Grafana**: Displays metrics and logs visualizations from Prometheus for real-time monitoring.
- **Alerting**: Alerts are configured based on metrics collected by Prometheus, and notifications are sent to Slack.

## Infrastructure as Code

### Kubernetes with Helm

Helm charts are used to deploy applications in Kubernetes. The `Helm` package manager is responsible for managing the Kubernetes manifests. The application is deployed using ArgoCD for continuous delivery and GitOps practices.

### Ansible for Infrastructure Automation

Ansible is used to automate the provisioning of the infrastructure, including setting up the Kubernetes cluster, installing dependencies, and managing configurations.

## Security and Secrets Management

### HashiCorp Vault

Secrets such as database credentials, API keys, and Docker registry credentials are stored in **HashiCorp Vault**. Jenkins retrieves these secrets securely from Vault during the pipeline execution, ensuring that sensitive data is never exposed in the source code.

### Nexus Repository for Artifact Storage

Nexus is used as a repository for storing Docker images. The images are tagged with the Jenkins build number and pushed to Nexus for version control.

## CI/CD Details

### Jenkinsfile

The `Jenkinsfile` defines the stages of the CI/CD pipeline, which include:

1. **SCM Checkout**: Checkout code from GitLab.
2. **Install Dependencies**: Install necessary dependencies.
3. **SonarQube Analysis**: Perform code quality analysis using SonarQube.
4. **Docker Image Build**: Build a Docker image from the Dockerfile.
5. **Push Image to Nexus**: Push the Docker image to Nexus Docker registry.
6. **Kubernetes Deployment**: Deploy the Docker image to Kubernetes.

## Deployment

### Kubernetes Deployment

The application is deployed using Helm, which handles Kubernetes deployments and makes rollbacks and scaling easier.

The deployment process ensures that the application is always running the latest Docker image from Nexus.

## License

This project is licensed under the **GNU GENERAL PUBLIC LICENSE** - see the [LICENSE](LICENSE) file for details.
