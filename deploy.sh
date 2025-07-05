#!/bin/bash

# PeerAI IPFS Deployment Script
# سكريبت نشر PeerAI على IPFS

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEPLOYMENT_TYPE="${1:-local}"
NODE_ID="${2:-peerai-node-$(date +%s)}"

# Logging
LOG_FILE="$PROJECT_DIR/deployment.log"

log() {
    local level=$1
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "[$timestamp] $level: $message" | tee -a "$LOG_FILE"
}

log_info() { log "INFO" "$*"; }
log_success() { log "SUCCESS" "$*"; }
log_warning() { log "WARNING" "$*"; }
log_error() { log "ERROR" "$*"; }

# Check system requirements
check_requirements() {
    log_info "🔍 Checking system requirements..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is not installed. Please install Python 3 first."
        exit 1
    fi
    
    log_success "✅ System requirements met"
}

# Generate SSL certificates for local development
generate_ssl_certs() {
    log_info "🔐 Generating SSL certificates..."
    
    mkdir -p ssl
    
    # Generate self-signed certificate
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout ssl/key.pem \
        -out ssl/cert.pem \
        -subj "/C=US/ST=State/L=City/O=PeerAI/CN=localhost"
    
    log_success "✅ SSL certificates generated"
}

# Deploy using Docker Compose
deploy_docker() {
    log_info "🐳 Deploying with Docker Compose..."
    
    # Set environment variables
    export NODE_ID="$NODE_ID"
    export DEPLOYMENT_TYPE="$DEPLOYMENT_TYPE"
    
    # Generate SSL certificates if they don't exist
    if [ ! -f "ssl/cert.pem" ] || [ ! -f "ssl/key.pem" ]; then
        generate_ssl_certs
    fi
    
    # Start services
    docker-compose -f docker-compose.ipfs.yml up -d
    
    log_success "✅ Docker deployment completed"
    log_info "📊 Services status:"
    docker-compose -f docker-compose.ipfs.yml ps
}

# Deploy locally without Docker
deploy_local() {
    log_info "🏠 Deploying locally..."
    
    # Check if IPFS is installed
    if ! command -v ipfs &> /dev/null; then
        log_info "📦 Installing IPFS..."
        
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            brew install ipfs
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            # Linux
            wget https://dist.ipfs.tech/go-ipfs/v0.23.0/go-ipfs_v0.23.0_linux-amd64.tar.gz
            tar -xvzf go-ipfs_v0.23.0_linux-amd64.tar.gz
            cd go-ipfs
            sudo bash install.sh
            cd ..
            rm -rf go-ipfs go-ipfs_v0.23.0_linux-amd64.tar.gz
        else
            log_error "Unsupported operating system: $OSTYPE"
            exit 1
        fi
    fi
    
    # Initialize IPFS if not already done
    if [ ! -d "$HOME/.ipfs" ]; then
        log_info "🔧 Initializing IPFS..."
        ipfs init --profile=server
    fi
    
    # Start IPFS daemon in background
    log_info "🚀 Starting IPFS daemon..."
    ipfs daemon --enable-pubsub-experiment &
    IPFS_PID=$!
    
    # Wait for IPFS to be ready
    sleep 10
    
    # Install Python dependencies
    log_info "📦 Installing Python dependencies..."
    pip install -r requirements_ipfs.txt
    pip install -r requirements_p2p_ai.txt
    
    # Start PeerAI application
    log_info "🤖 Starting PeerAI application..."
    export NODE_ID="$NODE_ID"
    export IPFS_HOST="localhost"
    export IPFS_PORT="5001"
    
    python3 app.py &
    PEERAI_PID=$!
    
    # Save PIDs for cleanup
    echo "$IPFS_PID" > .ipfs.pid
    echo "$PEERAI_PID" > .peerai.pid
    
    log_success "✅ Local deployment completed"
    log_info "📊 Services running:"
    log_info "   IPFS Daemon (PID: $IPFS_PID)"
    log_info "   PeerAI App (PID: $PEERAI_PID)"
}

# Deploy to cloud (VPS)
deploy_cloud() {
    log_info "☁️  Deploying to cloud..."
    
    # This would typically involve:
    # 1. SSH to remote server
    # 2. Clone repository
    # 3. Run docker-compose
    # 4. Configure firewall
    
    log_warning "Cloud deployment requires manual setup"
    log_info "Steps for cloud deployment:"
    log_info "1. SSH to your VPS"
    log_info "2. Clone this repository"
    log_info "3. Run: ./deploy.sh docker"
    log_info "4. Configure firewall to open ports 80, 443, 4001, 5001, 8080"
}

# Health check
health_check() {
    log_info "🏥 Performing health check..."
    
    # Check IPFS
    if curl -s http://localhost:5001/api/v0/version > /dev/null; then
        log_success "✅ IPFS API is responding"
    else
        log_error "❌ IPFS API is not responding"
    fi
    
    # Check PeerAI
    if curl -s http://localhost:8000/health > /dev/null; then
        log_success "✅ PeerAI API is responding"
    else
        log_error "❌ PeerAI API is not responding"
    fi
    
    # Check IPFS Gateway
    if curl -s http://localhost:8080 > /dev/null; then
        log_success "✅ IPFS Gateway is responding"
    else
        log_error "❌ IPFS Gateway is not responding"
    fi
}

# Stop services
stop_services() {
    log_info "🛑 Stopping services..."
    
    if [ "$DEPLOYMENT_TYPE" = "docker" ]; then
        docker-compose -f docker-compose.ipfs.yml down
        log_success "✅ Docker services stopped"
    else
        # Stop local services
        if [ -f .ipfs.pid ]; then
            kill $(cat .ipfs.pid) 2>/dev/null || true
            rm .ipfs.pid
        fi
        
        if [ -f .peerai.pid ]; then
            kill $(cat .peerai.pid) 2>/dev/null || true
            rm .peerai.pid
        fi
        
        log_success "✅ Local services stopped"
    fi
}

# Clean up
cleanup() {
    log_info "🧹 Cleaning up..."
    
    stop_services
    
    if [ "$DEPLOYMENT_TYPE" = "docker" ]; then
        docker-compose -f docker-compose.ipfs.yml down -v
        docker system prune -f
    fi
    
    log_success "✅ Cleanup completed"
}

# Show status
show_status() {
    log_info "📊 Deployment Status:"
    
    if [ "$DEPLOYMENT_TYPE" = "docker" ]; then
        docker-compose -f docker-compose.ipfs.yml ps
    else
        if [ -f .ipfs.pid ] && ps -p $(cat .ipfs.pid) > /dev/null; then
            log_success "✅ IPFS daemon is running (PID: $(cat .ipfs.pid))"
        else
            log_error "❌ IPFS daemon is not running"
        fi
        
        if [ -f .peerai.pid ] && ps -p $(cat .peerai.pid) > /dev/null; then
            log_success "✅ PeerAI application is running (PID: $(cat .peerai.pid))"
        else
            log_error "❌ PeerAI application is not running"
        fi
    fi
    
    echo ""
    log_info "🌐 Access URLs:"
    log_info "   PeerAI Web UI: http://localhost:8001"
    log_info "   PeerAI API: http://localhost:8000"
    log_info "   IPFS Gateway: http://localhost:8080"
    log_info "   IPFS API: http://localhost:5001"
}

# Main deployment logic
main() {
    log_info "🚀 Starting PeerAI IPFS deployment..."
    log_info "📋 Deployment type: $DEPLOYMENT_TYPE"
    log_info "🆔 Node ID: $NODE_ID"
    
    check_requirements
    
    case "$DEPLOYMENT_TYPE" in
        "docker")
            deploy_docker
            ;;
        "local")
            deploy_local
            ;;
        "cloud")
            deploy_cloud
            ;;
        "stop")
            stop_services
            exit 0
            ;;
        "cleanup")
            cleanup
            exit 0
            ;;
        "status")
            show_status
            exit 0
            ;;
        "health")
            health_check
            exit 0
            ;;
        *)
            log_error "Invalid deployment type: $DEPLOYMENT_TYPE"
            log_info "Usage: $0 {docker|local|cloud|stop|cleanup|status|health} [node_id]"
            exit 1
            ;;
    esac
    
    # Wait a bit for services to start
    sleep 5
    
    # Perform health check
    health_check
    
    # Show status
    show_status
    
    log_success "🎉 Deployment completed successfully!"
}

# Handle script interruption
trap 'log_error "Deployment interrupted"; exit 1' INT TERM

# Run main function
main "$@" 