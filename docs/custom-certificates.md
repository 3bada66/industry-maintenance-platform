# Custom Certificates Deployment Guide

This guide explains how to deploy Industry Maintenance Platform with custom certificates for internal deployments where Let's Encrypt is not practical (e.g., internal CA, self-signed certificates).

## Overview

For internal deployments, you might need to use:
- **Internal CA certificates** (e.g., corporate PKI)
- **Self-signed certificates** for testing
- **Wildcard certificates** for multiple subdomains
- **Custom certificate chains** with intermediate certificates

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- Custom certificates (certificate, private key, CA)
- Domain name pointing to your server

## Quick Start

### Nginx with Custom Certificates (Recommended)

Nginx is simpler and more reliable for custom certificates:

```bash
# 1. Setup certificates
make custom-certs-setup

# 2. Start services
make custom-certs-start

# 3. Access application
# Frontend: https://imp.local
# API: https://imp.local/api
```

### Traefik with Let's Encrypt (For Public Domains)

For public domains, use Traefik with Let's Encrypt:

```bash
# 1. Start production services
make prod

# 2. Access application
# Frontend: https://imp.local
# API: https://imp.local/api
# Traefik Dashboard: https://traefik.imp.local
```

### Step 1: Prepare Your Certificates

Ensure you have the following files:
- **Certificate file** (`.crt` or `.pem`)
- **Private key file** (`.key` or `.pem`)
- **CA certificate** (`.crt` or `.pem`)
- **Optional**: Certificate chain (intermediate certificates)

### Step 2: Configure Environment

```bash
# Copy the example configuration
cp custom-certs.env.example custom-certs.env

# Edit the configuration
nano custom-certs.env
```

Update the following variables:
```bash
# Domain configuration
DOMAIN=industry-maintenance-platform.internal
WWW_DOMAIN=www.industry-maintenance-platform.internal

# Certificate paths (absolute paths on the host)
CERT_PATH=/path/to/your/certificate.crt
KEY_PATH=/path/to/your/private.key
CA_PATH=/path/to/your/ca.crt

# Optional: Certificate chain
CHAIN_PATH=/path/to/your/chain.crt

# Traefik dashboard
TRAEFIK_DOMAIN=traefik.industry-maintenance-platform.internal
```

### Step 3: Validate Configuration

```bash
# Run the setup script to validate your configuration
./setup-custom-certs.sh
```

The script will:
- ✅ Validate certificate files exist
- ✅ Check certificate format
- ✅ Verify certificate-key pair match
- ✅ Check certificate expiration
- ✅ Set proper permissions
- ✅ Verify Docker environment

### Step 4: Deploy

```bash
# Start the services
docker-compose -f docker-compose.custom-certs.yml --env-file custom-certs.env up -d

# Check the logs
docker-compose -f docker-compose.custom-certs.yml logs -f
```

### Step 5: Access Your Application

- **Application**: https://industry-maintenance-platform.internal
- **API Documentation**: https://industry-maintenance-platform.internal/docs
- **Traefik Dashboard**: https://traefik.industry-maintenance-platform.internal

## Certificate Requirements

### Supported Formats

- **PEM format** (`.pem`, `.crt`, `.key`)
- **X.509 certificates**
- **RSA private keys** (2048+ bits recommended)
- **ECDSA private keys** (P-256, P-384, P-521)

### Certificate Validation

The setup script validates:
- Certificate format and validity
- Private key format and validity
- Certificate-key pair matching
- Certificate expiration (warns if < 30 days)
- File permissions and accessibility

### Security Recommendations

1. **Use strong private keys** (RSA 2048+ or ECDSA P-256+)
2. **Set proper file permissions** (600 for private keys)
3. **Store certificates securely** (encrypted storage, restricted access)
4. **Monitor certificate expiration** (set up alerts)
5. **Use certificate chains** for intermediate certificates

## Configuration Examples

### Internal CA Certificate

```bash
# custom-certs.env
DOMAIN=industry-maintenance-platform.company.local
CERT_PATH=/etc/ssl/certs/industry-maintenance-platform.company.local.crt
KEY_PATH=/etc/ssl/private/industry-maintenance-platform.company.local.key
CA_PATH=/etc/ssl/certs/company-ca.crt
CHAIN_PATH=/etc/ssl/certs/company-intermediate.crt
```

### Self-Signed Certificate

```bash
# custom-certs.env
DOMAIN=imp.local
CERT_PATH=/home/user/certs/imp.local.crt
KEY_PATH=/home/user/certs/imp.local.key
CA_PATH=/home/user/certs/imp.local.crt  # Self-signed
```

### Wildcard Certificate

```bash
# custom-certs.env
DOMAIN=*.company.local
CERT_PATH=/etc/ssl/certs/wildcard.company.local.crt
KEY_PATH=/etc/ssl/private/wildcard.company.local.key
CA_PATH=/etc/ssl/certs/company-ca.crt
```

## Troubleshooting

### Common Issues

#### Certificate Not Found
```bash
# Check if certificate files exist
ls -la /path/to/your/certificate.crt
ls -la /path/to/your/private.key
ls -la /path/to/your/ca.crt
```

#### Invalid Certificate Format
```bash
# Validate certificate format
openssl x509 -in /path/to/certificate.crt -text -noout

# Validate private key format
openssl rsa -in /path/to/private.key -check -noout
```

#### Certificate-Key Mismatch
```bash
# Check if certificate and key match
openssl x509 -noout -modulus -in certificate.crt | openssl md5
openssl rsa -noout -modulus -in private.key | openssl md5
```

#### Permission Denied
```bash
# Set proper permissions
chmod 600 /path/to/private.key
chmod 644 /path/to/certificate.crt
chmod 644 /path/to/ca.crt
```

### Docker Issues

#### Container Won't Start
```bash
# Check Docker logs
docker-compose -f docker-compose.custom-certs.yml logs traefik

# Check if certificates are mounted correctly
docker-compose -f docker-compose.custom-certs.yml exec traefik ls -la /etc/traefik/certs/
```

#### Certificate Not Loading
```bash
# Verify certificate mounting
docker-compose -f docker-compose.custom-certs.yml exec traefik cat /etc/traefik/certs/cert.crt

# Check Traefik configuration
docker-compose -f docker-compose.custom-certs.yml exec traefik cat /etc/traefik/traefik.yml
```

### Network Issues

#### SSL Handshake Failed
```bash
# Test SSL connection
openssl s_client -connect industry-maintenance-platform.internal:443 -servername industry-maintenance-platform.internal

# Check certificate chain
openssl s_client -connect industry-maintenance-platform.internal:443 -showcerts
```

#### DNS Resolution
```bash
# Check DNS resolution
nslookup industry-maintenance-platform.internal
dig industry-maintenance-platform.internal

# Test with curl
curl -v https://industry-maintenance-platform.internal
```

## Advanced Configuration

### Custom Traefik Configuration

If you need more advanced Traefik configuration, you can create a custom `traefik.yml`:

```yaml
# traefik-custom.yml
api:
  dashboard: true
  insecure: false

entryPoints:
  web:
    address: ":80"
    http:
      redirections:
        entrypoint:
          to: websecure
          scheme: https
  websecure:
    address: ":443"

providers:
  docker:
    endpoint: "unix:///var/run/docker.sock"
    exposedByDefault: false
  file:
    directory: /etc/traefik/certs
    watch: true

certificatesResolvers:
  letsencrypt:
    acme:
      tlsChallenge: {}
      email: admin@industry-maintenance-platform.internal
      storage: /letsencrypt/acme.json
```

Then mount it in your docker-compose:

```yaml
volumes:
  - "./traefik-custom.yml:/etc/traefik/traefik.yml:ro"
```

### Multiple Domains

To support multiple domains, update your configuration:

```bash
# custom-certs.env
DOMAIN=industry-maintenance-platform.internal
WWW_DOMAIN=www.industry-maintenance-platform.internal
API_DOMAIN=api.industry-maintenance-platform.internal
```

And add additional Traefik labels:

```yaml
labels:
  - "traefik.http.routers.backend.rule=Host(`api.industry-maintenance-platform.internal`) && PathPrefix(`/api`)"
  - "traefik.http.routers.frontend.rule=Host(`industry-maintenance-platform.internal`) || Host(`www.industry-maintenance-platform.internal`)"
```

## Security Considerations

### Certificate Management

1. **Regular Updates**: Keep certificates updated and monitor expiration
2. **Secure Storage**: Store private keys in encrypted storage
3. **Access Control**: Limit access to certificate files
4. **Backup Strategy**: Implement secure backup procedures
5. **Monitoring**: Set up alerts for certificate expiration

### Network Security

1. **Firewall Rules**: Configure appropriate firewall rules
2. **Network Isolation**: Use private networks for internal communication
3. **TLS Configuration**: Use strong TLS configurations
4. **Security Headers**: Implement security headers via Traefik

### Compliance

1. **Audit Logs**: Enable audit logging for certificate access
2. **Documentation**: Document certificate management procedures
3. **Testing**: Regular testing of certificate validity
4. **Incident Response**: Plan for certificate-related incidents

## Monitoring and Maintenance

### Certificate Monitoring

```bash
# Check certificate expiration
openssl x509 -in /path/to/certificate.crt -noout -dates

# Monitor certificate validity
./setup-custom-certs.sh
```

### Log Monitoring

```bash
# Monitor Traefik logs
docker-compose -f docker-compose.custom-certs.yml logs -f traefik

# Monitor application logs
docker-compose -f docker-compose.custom-certs.yml logs -f backend
docker-compose -f docker-compose.custom-certs.yml logs -f frontend
```

### Health Checks

```bash
# Check service health
docker-compose -f docker-compose.custom-certs.yml ps

# Test HTTPS connectivity
curl -I https://industry-maintenance-platform.internal

# Test API connectivity
curl -I https://industry-maintenance-platform.internal/api/health
```

## Support

If you encounter issues with custom certificates:

1. **Check the logs**: `docker-compose -f docker-compose.custom-certs.yml logs`
2. **Validate certificates**: `./setup-custom-certs.sh`
3. **Test connectivity**: `openssl s_client -connect your-domain:443`
4. **Review configuration**: Check `custom-certs.env` and `docker-compose.custom-certs.yml`

For additional support, please refer to the [main documentation](README.md) or create an issue on GitHub.
