# Infrastructure Configuration Repository

This repository contains the infrastructure configuration for setting up and managing development and DevOps tools. It includes Docker Compose configurations, Ansible playbooks, and associated configuration files.

## Repository Structure

```
.
├── Ansible/                  # Automation playbooks
│   ├── playbook_docker.yaml # Docker installation and setup
│   ├── playbook_helm.yaml   # Helm installation
│   └── playbook_k8s.yaml    # Kubernetes setup
├── config.hcl               # Vault server configuration
├── docker-compose.yaml      # Main services configuration
└── nginx/                   # Reverse proxy configuration
    ├── docker-compose.yaml
    └── nginx.conf
```

## Prerequisites

- Host machine running Linux (recommended Ubuntu 20.04 or later)
- Docker and Docker Compose installed
- Network access to 10.4.0.0/24 subnet
- SSL certificates (domain.crt and domain.key)
- System requirements:
  - Minimum 16GB RAM
  - 4+ CPU cores
  - 100GB+ available storage

## Network Configuration

- Host IP: 10.4.0.19
- All services run on the `goofy-network` (bridge network)
- Services are accessible via `.hdo3.local` domains

## Services

### HashiCorp Vault (vault.hdo3.local)

- Ports: 8200, 8201
- Handles secrets management
- Uses custom configuration from config.hcl

### GitLab CE (git.hdo3.local)

- Ports: 80 (9090), 443, 22 (2222)
- Self-hosted Git repository
- Configured with external URL

### Jenkins (jenkins.hdo3.local)

- Ports: 8080, 50000
- Custom image with Docker support
- Integrated with Docker-in-Docker

### SonarQube (sonar.hdo3.local)

- Port: 9000
- PostgreSQL database backend
- Community edition

### Nexus Repository (nexus.hdo3.local)

- Ports: 8081, 8085, 8443
- Docker registry available

### Docker-in-Docker

- Port: 2376
- TLS enabled
- Configured for Jenkins integration
- Custom CA certificate for Nexus registry

### PostgreSQL

- Internal service for SonarQube

## Ansible Playbooks

- `playbook_docker.yaml`: Installs and configures Docker
- `playbook_helm.yaml`: Installs Helm package manager
- `playbook_k8s.yaml`: Sets up Kubernetes prerequisites

To run playbooks:

```bash
ansible-playbook -i inventory.yaml playbook_<name>.yaml
```

## Security Considerations

- SSL certificates are required for secure communication
- Default credentials should be changed after initial setup
- Network access should be restricted to trusted sources
- Vault should be initialized and unsealed after deployment

## Troubleshooting

1. Service connectivity issues:
   - Verify network connectivity
   - Check SSL certificate configuration
   - Ensure services are running (`docker-compose ps`)

2. Docker-in-Docker issues:
   - Verify TLS configuration
   - Check certificate paths
   - Ensure privileged mode is enabled
