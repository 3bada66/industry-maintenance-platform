#!/bin/bash

# Script di deployment per Industry Maintenance Platform
# Utilizzo: ./deploy.sh [environment]

set -e

ENVIRONMENT=${1:-production}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🚀 Deploying Industry Maintenance Platform to $ENVIRONMENT environment..."

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Funzione per logging
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verifica prerequisiti
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Verifica Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed"
        exit 1
    fi
    
    # Verifica Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed"
        exit 1
    fi
    
    # Verifica file di configurazione
    if [ ! -f "$PROJECT_ROOT/backend/production.env.example" ]; then
        log_error "Production environment file not found"
        exit 1
    fi
    
    log_info "Prerequisites check passed"
}

# Setup ambiente
setup_environment() {
    log_info "Setting up environment..."
    
    cd "$PROJECT_ROOT"
    
    # Copia file di configurazione se non esistono
    if [ ! -f "backend/.env" ]; then
        log_warn "Creating .env file from example..."
        cp backend/production.env.example backend/.env
        log_warn "Please edit backend/.env with your production settings"
    fi
    
    # Crea directory per uploads se non esistono
    mkdir -p uploads/{documents,photos,prints}
    mkdir -p logs
    
    # Imposta permessi
    chmod 755 uploads
    chmod 755 logs
    
    log_info "Environment setup completed"
}

# Build delle immagini
build_images() {
    log_info "Building Docker images..."
    
    cd "$PROJECT_ROOT"
    
    # Build backend
    log_info "Building backend image..."
    docker build -t industry-maintenance-platform-backend:latest ./backend
    
    # Build frontend
    log_info "Building frontend image..."
    docker build -t industry-maintenance-platform-frontend:latest ./frontend
    
    log_info "Docker images built successfully"
}

# Database migration
run_migrations() {
    log_info "Running database migrations..."
    
    cd "$PROJECT_ROOT"
    
    # Avvia solo il database per le migrazioni
    docker-compose up -d db
    
    # Aspetta che il database sia pronto
    log_info "Waiting for database to be ready..."
    sleep 10
    
    # Esegui migrazioni
    docker-compose run --rm backend alembic upgrade head
    
    log_info "Database migrations completed"
}

# Deploy applicazione
deploy_application() {
    log_info "Deploying application..."
    
    cd "$PROJECT_ROOT"
    
    # Stop servizi esistenti
    docker-compose down
    
    # Avvia tutti i servizi
    docker-compose up -d
    
    log_info "Application deployed successfully"
}

# Health check
health_check() {
    log_info "Performing health check..."
    
    # Aspetta che i servizi siano pronti
    sleep 15
    
    # Test backend
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        log_info "Backend health check passed"
    else
        log_error "Backend health check failed"
        return 1
    fi
    
    # Test frontend
    if curl -f http://localhost:5173 > /dev/null 2>&1; then
        log_info "Frontend health check passed"
    else
        log_error "Frontend health check failed"
        return 1
    fi
    
    log_info "All health checks passed"
}

# Backup database
backup_database() {
    log_info "Creating database backup..."
    
    cd "$PROJECT_ROOT"
    
    BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    
    # Backup del database
    docker-compose exec -T db pg_dump -U industry-maintenance-platform_user industry-maintenance-platform > "$BACKUP_DIR/database.sql"
    
    # Backup degli uploads
    tar -czf "$BACKUP_DIR/uploads.tar.gz" uploads/
    
    log_info "Backup created in $BACKUP_DIR"
}

# Main deployment process
main() {
    log_info "Starting Industry Maintenance Platform deployment..."
    
    check_prerequisites
    setup_environment
    build_images
    
    # Backup se non è il primo deploy
    if docker-compose ps db | grep -q "Up"; then
        backup_database
    fi
    
    run_migrations
    deploy_application
    health_check
    
    log_info "🎉 Deployment completed successfully!"
    log_info "Backend: http://localhost:8000"
    log_info "Frontend: http://localhost:5173"
    log_info "API Docs: http://localhost:8000/docs"
}

# Gestione errori
trap 'log_error "Deployment failed. Check logs for details."; exit 1' ERR

# Esegui deployment
main "$@" 