# 🚀 PeerAI IPFS Deployment Guide

Complete guide for deploying PeerAI with IPFS integration across different environments.

## 📋 Quick Start

### Option 1: One-Command Deployment (Recommended)

```bash
# Deploy locally with Docker
./deploy.sh docker

# Deploy locally without Docker
./deploy.sh local

# Check status
./deploy.sh status

# Stop services
./deploy.sh stop
```

### Option 2: Using CLI Tool

```bash
# Install dependencies
pip install -r requirements_ipfs.txt

# Check system requirements
python ipfs_cli.py check

# Deploy
python ipfs_cli.py deploy start --type docker

# Manage models
python ipfs_cli.py model train --model-type bert --epochs 5
python ipfs_cli.py model list-models
```

## 🏗️ Deployment Options

### 🐳 Docker Deployment (Recommended)

**Best for:** Production, consistent environments, easy scaling

```bash
# Start all services
docker-compose -f docker-compose.ipfs.yml up -d

# View logs
docker-compose -f docker-compose.ipfs.yml logs -f

# Stop services
docker-compose -f docker-compose.ipfs.yml down
```

**Services included:**
- IPFS Node (Kubo)
- IPFS Cluster (for replication)
- PeerAI Application
- Redis (caching)
- Nginx (reverse proxy with SSL)

### 🏠 Local Deployment

**Best for:** Development, testing, learning

```bash
# Install IPFS
brew install ipfs  # macOS
# or
wget https://dist.ipfs.tech/go-ipfs/v0.23.0/go-ipfs_v0.23.0_linux-amd64.tar.gz  # Linux

# Initialize IPFS
ipfs init --profile=server

# Start IPFS daemon
ipfs daemon --enable-pubsub-experiment &

# Install Python dependencies
pip install -r requirements_ipfs.txt

# Start PeerAI
python app.py
```

### ☁️ Cloud Deployment (VPS)

**Best for:** Public nodes, production servers

1. **Choose a VPS provider:**
   - DigitalOcean
   - Hetzner
   - AWS EC2
   - Google Cloud

2. **Server requirements:**
   - 2+ CPU cores
   - 4GB+ RAM
   - 50GB+ storage
   - Ubuntu 20.04+ or CentOS 8+

3. **Deploy:**
```bash
# SSH to your server
ssh user@your-server-ip

# Clone repository
git clone <your-repo-url>
cd PeerAI

# Deploy with Docker
./deploy.sh docker

# Configure firewall
sudo ufw allow 80,443,4001,5001,8080
```

## 🔧 Configuration

### Environment Variables

```bash
# IPFS Configuration
IPFS_HOST=localhost          # IPFS node host
IPFS_PORT=5001              # IPFS API port
NODE_ID=peerai-node-001     # Unique node identifier

# PeerAI Configuration
LOG_LEVEL=INFO              # Logging level
MODEL_STORAGE_PATH=./models # Model storage directory
DATA_STORAGE_PATH=./data    # Data storage directory
```

### IPFS Configuration

```bash
# Initialize with server profile
ipfs init --profile=server

# Configure IPFS for better performance
ipfs config --json API.HTTPHeaders.Access-Control-Allow-Origin '["*"]'
ipfs config --json API.HTTPHeaders.Access-Control-Allow-Methods '["PUT", "POST", "GET"]'
ipfs config --json API.HTTPHeaders.Access-Control-Allow-Headers '["Authorization"]'

# Enable pubsub for real-time features
ipfs daemon --enable-pubsub-experiment
```

## 📊 Monitoring & Health Checks

### Health Check Endpoints

```bash
# PeerAI Health
curl http://localhost:8000/health

# IPFS API
curl http://localhost:5001/api/v0/version

# IPFS Gateway
curl http://localhost:8080
```

### Using the CLI

```bash
# Check system health
python ipfs_cli.py deploy health

# View deployment status
python ipfs_cli.py deploy status

# Check IPFS node info
python ipfs_cli.py ipfs info
```

## 🤖 Model Management

### Training & Deploying Models

```bash
# Train a model and deploy to IPFS
python ipfs_cli.py model train \
  --model-type bert \
  --epochs 10 \
  --description "Arabic sentiment analysis model"

# List available models
python ipfs_cli.py model list-models

# Download a model
python ipfs_cli.py model download <CID>
```

### Data Management

```bash
# Upload dataset to IPFS
python ipfs_cli.py data upload sample_data/iris.csv \
  --data-type csv \
  --description "Iris flower dataset"

# List available datasets
python ipfs_cli.py data list-datasets
```

## 🔒 Security Considerations

### SSL/TLS Configuration

```bash
# Generate SSL certificates (for production)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ssl/key.pem \
  -out ssl/cert.pem \
  -subj "/C=US/ST=State/L=City/O=PeerAI/CN=your-domain.com"
```

### Firewall Configuration

```bash
# Allow necessary ports
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw allow 4001/tcp # IPFS P2P
sudo ufw allow 5001/tcp # IPFS API
sudo ufw allow 8080/tcp # IPFS Gateway
```

### Access Control

```bash
# Configure IPFS API access
ipfs config --json API.HTTPHeaders.Access-Control-Allow-Origin '["https://your-domain.com"]'

# Use authentication for sensitive endpoints
# (implement in your application)
```

## 🚨 Troubleshooting

### Common Issues

1. **IPFS not starting:**
```bash
# Check if IPFS is already running
ps aux | grep ipfs

# Kill existing process
pkill ipfs

# Restart
ipfs daemon --enable-pubsub-experiment
```

2. **Port conflicts:**
```bash
# Check what's using the port
sudo lsof -i :5001

# Change IPFS port in configuration
ipfs config Addresses.API /ip4/0.0.0.0/tcp/5002
```

3. **Docker issues:**
```bash
# Clean up Docker
docker system prune -f
docker volume prune -f

# Rebuild containers
docker-compose -f docker-compose.ipfs.yml build --no-cache
```

### Logs & Debugging

```bash
# View PeerAI logs
tail -f deployment.log

# View Docker logs
docker-compose -f docker-compose.ipfs.yml logs -f peerai

# View IPFS logs
docker-compose -f docker-compose.ipfs.yml logs -f ipfs
```

## 📈 Scaling & Performance

### Horizontal Scaling

```bash
# Scale PeerAI instances
docker-compose -f docker-compose.ipfs.yml up -d --scale peerai=3

# Use load balancer
# Configure nginx for multiple backend instances
```

### Performance Optimization

```bash
# Configure IPFS for better performance
ipfs config --json Datastore.StorageMax "10GB"
ipfs config --json Datastore.StorageGCWatermark 90

# Enable IPFS garbage collection
ipfs repo gc
```

## 🔄 Backup & Recovery

### Backup IPFS Data

```bash
# Backup IPFS repository
tar -czf ipfs_backup_$(date +%Y%m%d).tar.gz ~/.ipfs

# Backup PeerAI data
tar -czf peerai_backup_$(date +%Y%m%d).tar.gz models/ data/
```

### Recovery

```bash
# Restore IPFS data
tar -xzf ipfs_backup_YYYYMMDD.tar.gz -C ~/

# Restore PeerAI data
tar -xzf peerai_backup_YYYYMMDD.tar.gz
```

## 🌐 Public Gateways

### Using Public IPFS Gateways

```bash
# Access content via public gateways
https://ipfs.io/ipfs/<CID>
https://gateway.pinata.cloud/ipfs/<CID>
https://cloudflare-ipfs.com/ipfs/<CID>
```

### Setting Up Your Own Gateway

```bash
# Configure nginx as IPFS gateway
# (see nginx.conf for configuration)

# Access your gateway
https://your-domain.com/ipfs/<CID>
```

## 📚 Additional Resources

- [IPFS Documentation](https://docs.ipfs.io/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PeerAI Documentation](link-to-your-docs)

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review logs in `deployment.log`
3. Open an issue on GitHub
4. Contact the development team

---

**Happy Deploying! 🚀** 