# Docker Deployment Guide

This guide explains how to deploy Industry Maintenance Platform using Docker Compose with Traefik as a reverse proxy, providing automatic HTTPS (Let's Encrypt) and secure routing for both frontend and backend.

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- A domain name (e.g., `industry-maintenance-platform.yourdomain.com`) pointing to your server's public IP
- (Optional) Email address for Let's Encrypt certificate registration

## Folder Structure

```
/industry-maintenance-platform
  /backend
  /frontend
  /letsencrypt   # (created automatically by Traefik)
  docker-compose.yml
  README.md
  ...
```

## Deployment Methods

### Method 1: Production Local (Recommended for first time)

#### Step 1: Start Production Environment
```bash
# Start production with Nginx + self-signed certificates + auto-init DB
make prod
```

**Access Points:**
- Frontend: https://localhost
- Backend API: https://localhost/api/docs

### Method 2: Production Cloud with Traefik (Recommended for production)

#### Step 1: DNS Setup
Create an A record for `industry-maintenance-platform.yourdomain.com` pointing to your server's public IP.

#### Step 2: Start Production Services
```bash
# Start production with Traefik + Let's Encrypt
make prod-cloud
```

**Access Points:**
- Application: https://imp.local
- Traefik Dashboard: http://localhost:8080

### Method 3: Custom Certificates with Nginx

#### Step 1: Setup Custom Certificates
```bash
# Setup custom certificates
make custom-certs-setup

# Start with custom certificates
make custom-certs-start
```

**Access Points:**
- Application: https://yourdomain.com

### Method 4: Manual Configuration (Advanced)

#### Step 1: Configure Environment
```bash
# Copy environment template
cp production.env.example production.env

# Edit configuration
nano production.env
```

Key environment variables:
```bash
# Frontend
VITE_API_URL=https://industry-maintenance-platform.yourdomain.com/api

# Backend
CORS_ORIGINS=https://industry-maintenance-platform.yourdomain.com
```

#### Step 2: Start Services
```bash
# Start all services
docker-compose up -d

# Verify services are running
docker-compose ps
```

#### Step 4: Access the Application
- **Application**: https://industry-maintenance-platform.yourdomain.com
- **API Documentation**: https://industry-maintenance-platform.yourdomain.com/docs
- **Traefik Dashboard**: http://your-server-ip:8080 (if enabled)

### Method 4: Development Setup (Advanced)

#### Local Development
```bash
# Start services for development
docker-compose -f docker-compose.dev.yml up -d

# Access services
# Frontend: http://localhost:5173
# Backend: http://localhost:8000
# Database: localhost:5432
```

#### Development with Hot Reload
```bash
# Start backend with hot reload
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Start frontend with hot reload
cd frontend
npm run dev
```

## Docker Compose Configuration

### Production Configuration

```yaml
version: '3.8'

services:
  traefik:
    image: traefik:v2.10
    container_name: traefik
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
      - "8080:8080"  # Dashboard (optional)
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./letsencrypt:/letsencrypt
    command:
      - "--api.dashboard=true"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.letsencrypt.acme.email=your-email@domain.com"
      - "--certificatesresolvers.letsencrypt.acme.storage=/letsencrypt/acme.json"
      - "--certificatesresolvers.letsencrypt.acme.httpchallenge.entrypoint=web"
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.traefik.rule=Host(`traefik.yourdomain.com`)"
      - "traefik.http.routers.traefik.entrypoints=websecure"
      - "traefik.http.routers.traefik.tls.certresolver=letsencrypt"

  db:
    image: postgres:15
    container_name: industry-maintenance-platform-db
    restart: unless-stopped
    environment:
      POSTGRES_DB: industry-maintenance-platform
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - industry-maintenance-platform-network

  backend:
    build: ./backend
    container_name: industry-maintenance-platform-backend
    restart: unless-stopped
    environment:
      - DATABASE_URL=postgresql://postgres:${DB_PASSWORD}@db:5432/industry-maintenance-platform
      - SECRET_KEY=${SECRET_KEY}
      - CORS_ORIGINS=${CORS_ORIGINS}
    volumes:
      - ./uploads:/app/uploads
    depends_on:
      - db
    networks:
      - industry-maintenance-platform-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.backend.rule=Host(`industry-maintenance-platform.yourdomain.com`) && PathPrefix(`/api`)"
      - "traefik.http.routers.backend.entrypoints=websecure"
      - "traefik.http.routers.backend.tls.certresolver=letsencrypt"
      - "traefik.http.services.backend.loadbalancer.server.port=8000"

  frontend:
    build: ./frontend
    container_name: industry-maintenance-platform-frontend
    restart: unless-stopped
    environment:
      - VITE_API_URL=https://industry-maintenance-platform.yourdomain.com/api
    networks:
      - industry-maintenance-platform-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.frontend.rule=Host(`industry-maintenance-platform.yourdomain.com`)"
      - "traefik.http.routers.frontend.entrypoints=websecure"
      - "traefik.http.routers.frontend.tls.certresolver=letsencrypt"
      - "traefik.http.services.frontend.loadbalancer.server.port=5173"

volumes:
  postgres_data:

networks:
  industry-maintenance-platform-network:
    driver: bridge
```

### Development Configuration

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    container_name: industry-maintenance-platform-db-dev
    environment:
      POSTGRES_DB: industry-maintenance-platform
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: development
    ports:
      - "5432:5432"
    volumes:
      - postgres_data_dev:/var/lib/postgresql/data

  backend:
    build: ./backend
    container_name: industry-maintenance-platform-backend-dev
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:development@db:5432/industry-maintenance-platform
      - SECRET_KEY=development-secret-key
      - CORS_ORIGINS=http://localhost:5173,http://localhost:3000
      - DEBUG=true
    volumes:
      - ./backend:/app
      - ./uploads:/app/uploads
    depends_on:
      - db
    command: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

  frontend:
    build: ./frontend
    container_name: industry-maintenance-platform-frontend-dev
    ports:
      - "5173:5173"
    environment:
      - VITE_API_URL=http://localhost:8000
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: npm run dev

volumes:
  postgres_data_dev:
```

## Security Configuration

### Production Security

#### Environment Variables
```bash
# Security
SECRET_KEY=your-very-secure-secret-key-here
JWT_ISSUER=industry-maintenance-platform-api
JWT_AUDIENCE=industry-maintenance-platform-client

# Database
DB_PASSWORD=your-secure-database-password

# CORS
CORS_ORIGINS=https://industry-maintenance-platform.yourdomain.com

# Cookies
SECURE_COOKIES=true
SAME_SITE_COOKIES=strict
```

#### Security Headers
```yaml
# Add to Traefik labels
- "traefik.http.middlewares.security.headers.stsIncludeSubdomains=true"
- "traefik.http.middlewares.security.headers.stsPreload=true"
- "traefik.http.middlewares.security.headers.stsSeconds=31536000"
- "traefik.http.middlewares.security.headers.contentTypeNosniff=true"
- "traefik.http.middlewares.security.headers.browserXssFilter=true"
- "traefik.http.middlewares.security.headers.referrerPolicy=strict-origin-when-cross-origin"
```

### Development Security

```bash
# Development environment variables
SECRET_KEY=development-secret-key
DEBUG=true
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
SECURE_COOKIES=false
```

## Monitoring and Logging

### Log Management

#### View Logs
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db

# Follow logs
docker-compose logs -f backend
```

#### Log Configuration
```yaml
# Add to services
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

### Health Checks

#### Service Health
```bash
# Check service status
docker-compose ps

# Check service health
curl http://localhost:8000/health
```

#### Database Health
```bash
# Check database connection
docker-compose exec db pg_isready -U postgres

# Check database size
docker-compose exec db psql -U postgres -d industry-maintenance-platform -c "SELECT pg_size_pretty(pg_database_size('industry-maintenance-platform'));"
```

## Backup and Restore

### Database Backup
```bash
# Create backup
docker-compose exec db pg_dump -U postgres industry-maintenance-platform > backup.sql

# Restore backup
docker-compose exec -T db psql -U postgres industry-maintenance-platform < backup.sql
```

### Volume Backup
```bash
# Backup volumes
docker run --rm -v industry-maintenance-platform_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_data.tar.gz -C /data .

# Restore volumes
docker run --rm -v industry-maintenance-platform_postgres_data:/data -v $(pwd):/backup alpine tar xzf /backup/postgres_data.tar.gz -C /data
```

## Troubleshooting

### Common Issues

#### Port Conflicts
```bash
# Check port usage
lsof -i :80
lsof -i :443
lsof -i :8000
lsof -i :5173

# Stop conflicting services
sudo systemctl stop nginx
sudo systemctl stop apache2
```

#### Certificate Issues
```bash
# Check Let's Encrypt logs
docker-compose logs traefik

# Check certificate files
ls -la letsencrypt/

# Restart Traefik
docker-compose restart traefik
```

#### Database Connection Issues
```bash
# Check database container
docker-compose ps db

# Check database logs
docker-compose logs db

# Restart database
docker-compose restart db
```

#### Frontend Build Issues
```bash
# Rebuild frontend
docker-compose build frontend

# Clear node_modules
docker-compose run --rm frontend rm -rf node_modules
docker-compose build frontend
```

### Performance Optimization

#### Resource Limits
```yaml
# Add to services
deploy:
  resources:
    limits:
      memory: 1G
      cpus: '0.5'
    reservations:
      memory: 512M
      cpus: '0.25'
```

#### Database Optimization
```yaml
# Add to db service
command: >
  postgres
  -c shared_buffers=256MB
  -c effective_cache_size=1GB
  -c maintenance_work_mem=64MB
  -c checkpoint_completion_target=0.9
  -c wal_buffers=16MB
  -c default_statistics_target=100
```

## Scaling

### Horizontal Scaling
```bash
# Scale backend services
docker-compose up -d --scale backend=3

# Scale with load balancer
docker-compose up -d --scale backend=3 --scale frontend=2
```

### Load Balancer Configuration
```yaml
# Add load balancer
nginx:
  image: nginx:alpine
  ports:
    - "80:80"
  volumes:
    - ./nginx.conf:/etc/nginx/nginx.conf
  depends_on:
    - backend
    - frontend
```

## Maintenance

### Regular Maintenance Tasks

#### Update Images
```bash
# Pull latest images
docker-compose pull

# Rebuild services
docker-compose build --no-cache

# Restart services
docker-compose up -d
```

#### Clean Up
```bash
# Remove unused images
docker image prune -f

# Remove unused volumes
docker volume prune -f

# Remove unused networks
docker network prune -f

# Complete cleanup
docker system prune -a -f
```

#### Database Maintenance
```bash
# Vacuum database
docker-compose exec db psql -U postgres -d industry-maintenance-platform -c "VACUUM ANALYZE;"

# Check database size
docker-compose exec db psql -U postgres -d industry-maintenance-platform -c "SELECT pg_size_pretty(pg_database_size('industry-maintenance-platform'));"
```

## Best Practices

### Security Best Practices
1. **Use strong passwords**: Generate secure passwords for all services
2. **Enable HTTPS**: Always use HTTPS in production
3. **Regular updates**: Keep Docker images updated
4. **Access control**: Limit access to Docker daemon
5. **Network isolation**: Use custom networks for service communication

### Performance Best Practices
1. **Resource limits**: Set appropriate resource limits
2. **Health checks**: Implement health checks for all services
3. **Logging**: Configure proper logging and rotation
4. **Backup strategy**: Implement regular backup procedures
5. **Monitoring**: Set up monitoring and alerting

### Development Best Practices
1. **Use volumes**: Mount source code for development
2. **Hot reload**: Enable hot reload for development
3. **Environment separation**: Use different configurations for dev/prod
4. **Version control**: Keep Docker configurations in version control
5. **Documentation**: Document all configuration changes 