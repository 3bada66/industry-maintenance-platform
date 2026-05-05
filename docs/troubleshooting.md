# Troubleshooting Guide

This guide provides solutions for common issues encountered when using Industry Maintenance Platform.

## Quick Commands Reference

### Using Make Commands (Recommended)
```bash
make status    # Check service status
make logs      # View all logs
make restart   # Restart all services
make clean     # Clean system completely
make prod      # Start production environment (Nginx + self-signed certificates + auto-init DB)
make prod-cloud # Start production environment (Traefik + Let's Encrypt)
make demo      # Add demo data
make shell     # Open backend shell
make migrate   # Run database migrations
make reset-db  # Reset database
make config    # Show configuration information
make traefik   # Show Traefik dashboard information
```

### Manual Docker Commands (Alternative)
```bash
# Development
docker-compose -f docker-compose.dev.yml ps
docker-compose -f docker-compose.dev.yml logs
docker-compose -f docker-compose.dev.yml restart
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.dev.yml up -d

# Production
docker-compose ps
docker-compose logs
docker-compose restart
docker-compose down
docker-compose up -d

# Custom Certificates
docker-compose -f docker-compose.custom-certs.yml ps
docker-compose -f docker-compose.custom-certs.yml logs
docker-compose -f docker-compose.custom-certs.yml restart
docker-compose -f docker-compose.custom-certs.yml down
docker-compose -f docker-compose.custom-certs.yml up -d
```

## Quick Diagnostics

### System Health Check
```bash
# Check if all services are running
make status

# Check system health
curl https://localhost/api/health  # Production Local
curl https://imp.local/api/health  # Production Cloud

# Check setup status
curl https://localhost/api/setup/status  # Production Local
curl https://imp.local/api/setup/status  # Production Cloud
```

### Log Analysis
```bash
# View all logs
make logs

# View specific service logs
# Development
docker-compose -f docker-compose.dev.yml logs backend
docker-compose -f docker-compose.dev.yml logs frontend

# Production
docker-compose logs backend
docker-compose logs frontend

# Custom Certificates
docker-compose -f docker-compose.custom-certs.yml logs backend
docker-compose -f docker-compose.custom-certs.yml logs frontend
```

## Common Issues

### Installation Issues

#### Port Conflicts
**Symptoms**: `Port is already allocated` or services fail to start

**Solution**:
```bash
# Check what's using the ports
lsof -i :8000
lsof -i :5173
lsof -i :5432
lsof -i :80
lsof -i :443

# Stop conflicting services
sudo systemctl stop nginx
sudo systemctl stop apache2
sudo systemctl stop postgresql

# Or change ports in docker-compose files
# Development: docker-compose.dev.yml
# Production: docker-compose.yml
# Custom Certificates: docker-compose.custom-certs.yml
```

#### Insufficient Permissions
**Symptoms**: `Permission denied` errors

**Solution**:
```bash
# Fix upload directory permissions
sudo chown -R 1000:1000 uploads/
sudo chmod -R 755 uploads/

# Fix Docker permissions
sudo chown -R $USER:$USER /var/run/docker.sock

# Add user to docker group (if needed)
sudo usermod -aG docker $USER

# Restart Docker service
sudo systemctl restart docker
```

### Database Issues

#### Database Connection Failed
**Symptoms**: `Database connection failed` or `Connection refused`

**Solution**:
```bash
# Check database container status
docker-compose ps db

# View database logs
docker-compose logs db

# Restart database
docker-compose restart db

# Or restart all services
make restart
```

#### Database Migration Issues
**Symptoms**: `Migration failed` or `Database schema error`

**Solution**:
```bash
# Run migrations manually
make migrate

# Or reset database
make reset-db

# Or clean and reinitialize
make clean
make prod
```

### Frontend Issues

#### Frontend Not Loading
**Symptoms**: `Frontend not loading` or `404 Not Found`

**Solution**:
```bash
# Check frontend container status
docker-compose ps frontend

# View frontend logs
docker-compose logs frontend

# Restart frontend
docker-compose restart frontend

# Or rebuild frontend
make rebuild
```

#### API Calls Failing
**Symptoms**: `API calls failing` or `CORS error`

**Solution**:
```bash
# Check backend container status
docker-compose ps backend

# View backend logs
docker-compose logs backend

# Check CORS configuration
make config

# Restart backend
docker-compose restart backend
```

### Backend Issues

#### Backend Not Starting
**Symptoms**: `Backend not starting` or `500 Internal Server Error`

**Solution**:
```bash
# Check backend container status
docker-compose ps backend

# View backend logs
docker-compose logs backend

# Check database connection
docker-compose ps db

# Restart backend
docker-compose restart backend
```

### Reverse Proxy Issues

#### Traefik Issues (Production)
**Symptoms**: `Traefik not working` or `SSL certificate error`

**Solution**:
```bash
# Check Traefik container status
docker-compose ps traefik

# View Traefik logs
docker-compose logs traefik

# Check Traefik dashboard
make traefik

# Restart Traefik
docker-compose restart traefik
```

#### Nginx Issues (Custom Certificates)
**Symptoms**: `Nginx not working` or `SSL certificate error`

**Solution**:
```bash
# Check Nginx container status
docker-compose -f docker-compose.custom-certs.yml ps nginx

# View Nginx logs
docker-compose -f docker-compose.custom-certs.yml logs nginx

# Check certificate files
ls -la test-certs/

# Restart Nginx
docker-compose -f docker-compose.custom-certs.yml restart nginx
```

### SPA Routing Issues

#### F5 Refresh Returns JSON Instead of Page
**Symptoms**: When refreshing the page (F5) on routes like `/assets`, `/sites`, etc., you get a JSON response instead of the Vue.js page.

**Root Cause**: Nginx is routing browser requests to the backend API instead of the frontend SPA.

**Solution**:
```bash
# Test the fix with the recommended method
make custom-certs-start

# Verify the fix works
curl -k -I https://imp.local/assets
# Should return: Content-Type: text/html (not application/json)

# Test API calls still work
curl -k -H "Accept: application/json" -I https://imp.local/assets
# Should return: Content-Type: application/json
```

**Note**: This issue is automatically resolved in the current nginx configuration, which intelligently distinguishes between API calls and browser requests.

### General Issues

#### Services Not Starting
**Symptoms**: `Services not starting` or `Container exit`

**Solution**:
```bash
# Check all container status
docker-compose ps

# View all logs
docker-compose logs

# Clean and restart
make clean
make prod

# Or for specific deployment
make prod-cloud
make custom-certs-start
```

#### Memory Issues
**Symptoms**: `Out of memory` or `Container killed`

**Solution**:
```bash
# Check system memory
free -h

# Check Docker memory usage
docker stats

# Increase Docker memory limit
# Edit Docker Desktop settings or /etc/docker/daemon.json

# Restart Docker
sudo systemctl restart docker
```

#### Disk Space Issues
**Symptoms**: `No space left on device` or `Disk full`

**Solution**:
```bash
# Check disk usage
df -h

# Clean Docker images
docker system prune -a

# Clean Docker volumes
docker volume prune

# Clean system
make clean
```

### Configuration Issues

#### CORS Issues
**Symptoms**: `CORS error` or `Cross-origin request blocked`

**Solution**:
```bash
# Check CORS configuration
make config

# Check environment variables
cat .env

# Restart services
make restart
```

#### SSL Certificate Issues
**Symptoms**: `SSL certificate error` or `Certificate not trusted`

**Solution**:
```bash
# Check certificate files
ls -la test-certs/

# Check certificate validity
openssl x509 -in test-certs/imp.local.crt -text -noout

# Regenerate certificates
make custom-certs-setup

# Restart services
make custom-certs-start
```

## Recovery Procedures

### Complete System Recovery
**Symptoms**: `Complete system failure` or `System not working`

**Solution**:
```bash
# Stop all services
make stop

# Clean system
make clean

# Reinitialize system
make prod

# Or for specific deployment
make prod-cloud
make custom-certs-start
```

### Database Recovery
**Symptoms**: `Database corruption` or `Database not working`

**Solution**:
```bash
# Stop services
make stop

# Clean database
docker-compose down -v

# Reinitialize database
make prod

# Or restore from backup
python scripts/restore.py backups/industry-maintenance-platform-backup-*.tar.gz
```

### Configuration Recovery
**Symptoms**: `Configuration corruption` or `Configuration not working`

**Solution**:
```bash
# Check configuration
make config

# Check environment files
cat .env

# Check docker-compose files
cat docker-compose.yml

# Restore from backup
cp production.env.example .env

# Restart services
make restart
```

## Support and Resources

### Getting Help
**Symptoms**: `Need help` or `Support needed`

**Solution**:
```bash
# Check documentation
ls -la docs/

# Check README
cat README.md

# Check troubleshooting
cat docs/troubleshooting.md

# Check configuration
make config

# Check system status
make status
```

### Reporting Issues
**Symptoms**: `Report issue` or `Bug report`

**Solution**:
```bash
# Collect system information
make status

# Collect configuration
make config

# Collect logs
make logs

# Collect system information
uname -a
docker --version
docker-compose --version
```

## Best Practices

### Regular Maintenance
**Symptoms**: `Regular maintenance` or `System maintenance`

**Solution**:
```bash
# Regular system check
make status

# Regular configuration check
make config

# Regular log check
make logs

# Regular backup
python scripts/backup.py

# Regular cleanup
make clean
```

### Security Best Practices
**Symptoms**: `Security best practices` or `Security maintenance`

**Solution**:
```bash
# Check security configuration
make config

# Check SSL certificates
ls -la letsencrypt/

# Check user permissions
docker-compose exec backend python -c "from app.database import get_db; from app.crud.users import get_user_by_email; print(get_user_by_email(next(get_db()), 'admin@example.com'))"

# Check role permissions
docker-compose exec backend python -c "from app.database import get_db; from app.crud.roles import get_role_by_name; print(get_role_by_name(next(get_db()), 'admin'))"
```

## Conclusion

This troubleshooting guide covers the most common issues encountered when using Industry Maintenance Platform. If you encounter an issue not covered here, please:

1. Check the logs: `make logs`
2. Check the configuration: `make config`
3. Check the system status: `make status`
4. Check the documentation: `docs/`
5. Report the issue with system information

For additional support, please contact:
- **Email**: obadahakeem74@gmail.com
- **Website**: https://localhost
- **GitHub**: https://localhost
