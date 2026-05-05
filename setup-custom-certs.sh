#!/bin/bash

# Setup script for custom certificates deployment
# This script helps you configure Industry Maintenance Platform with custom certificates

set -e

echo "🔐 Industry Maintenance Platform Custom Certificates Setup"
echo "======================================"

# Check if custom-certs.env exists
if [ ! -f "custom-certs.env" ]; then
    echo "❌ custom-certs.env not found!"
    echo "📋 Please copy custom-certs.env.example to custom-certs.env and configure it:"
    echo "   cp custom-certs.env.example custom-certs.env"
    echo "   nano custom-certs.env"
    exit 1
fi

# Load environment variables
source custom-certs.env

echo "📋 Configuration loaded:"
echo "   Domain: $DOMAIN"
echo "   Certificate: $CERT_PATH"
echo "   Private Key: $KEY_PATH"
echo "   CA: $CA_PATH"

# Validate certificate files exist
echo "🔍 Validating certificate files..."

if [ ! -f "$CERT_PATH" ]; then
    echo "❌ Certificate file not found: $CERT_PATH"
    exit 1
fi

if [ ! -f "$KEY_PATH" ]; then
    echo "❌ Private key file not found: $KEY_PATH"
    exit 1
fi

if [ ! -f "$CA_PATH" ]; then
    echo "❌ CA file not found: $CA_PATH"
    exit 1
fi

echo "✅ All certificate files found"

# Validate certificate format
echo "🔍 Validating certificate format..."

# Check certificate
if ! openssl x509 -in "$CERT_PATH" -text -noout > /dev/null 2>&1; then
    echo "❌ Invalid certificate format: $CERT_PATH"
    exit 1
fi

# Check private key
if ! openssl rsa -in "$KEY_PATH" -check -noout > /dev/null 2>&1; then
    echo "❌ Invalid private key format: $KEY_PATH"
    exit 1
fi

# Check CA
if ! openssl x509 -in "$CA_PATH" -text -noout > /dev/null 2>&1; then
    echo "❌ Invalid CA format: $CA_PATH"
    exit 1
fi

echo "✅ All certificate files are valid"

# Check if certificate matches private key
echo "🔍 Validating certificate-key pair..."

CERT_MODULUS=$(openssl x509 -noout -modulus -in "$CERT_PATH" | openssl md5)
KEY_MODULUS=$(openssl rsa -noout -modulus -in "$KEY_PATH" | openssl md5)

if [ "$CERT_MODULUS" != "$KEY_MODULUS" ]; then
    echo "❌ Certificate and private key do not match!"
    exit 1
fi

echo "✅ Certificate and private key match"

# Check certificate expiration
echo "🔍 Checking certificate expiration..."

CERT_END_DATE=$(openssl x509 -enddate -noout -in "$CERT_PATH" | cut -d= -f2)
# Handle different date formats (Linux vs macOS)
if date -d "$CERT_END_DATE" +%s > /dev/null 2>&1; then
    # Linux format
    CERT_END_EPOCH=$(date -d "$CERT_END_DATE" +%s)
elif date -j -f "%b %d %H:%M:%S %Y %Z" "$CERT_END_DATE" +%s > /dev/null 2>&1; then
    # macOS format
    CERT_END_EPOCH=$(date -j -f "%b %d %H:%M:%S %Y %Z" "$CERT_END_DATE" +%s)
else
    # Fallback: try to parse the date
    CERT_END_EPOCH=$(date -j -f "%b %d %H:%M:%S %Y" "$CERT_END_DATE" +%s 2>/dev/null || echo "0")
fi
CURRENT_EPOCH=$(date +%s)
DAYS_UNTIL_EXPIRY=$(( (CERT_END_EPOCH - CURRENT_EPOCH) / 86400 ))

if [ $DAYS_UNTIL_EXPIRY -lt 30 ]; then
    echo "⚠️  Warning: Certificate expires in $DAYS_UNTIL_EXPIRY days"
    echo "   Consider renewing your certificate soon"
else
    echo "✅ Certificate expires in $DAYS_UNTIL_EXPIRY days"
fi

# Create letsencrypt directory if it doesn't exist
mkdir -p letsencrypt

# Set proper permissions
chmod 600 "$CERT_PATH" "$KEY_PATH" "$CA_PATH"
chmod 755 letsencrypt

echo "✅ Permissions set correctly"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "✅ Docker is running"

# Check if docker-compose is available
if ! command -v docker-compose > /dev/null 2>&1; then
    echo "❌ docker-compose not found. Please install docker-compose and try again."
    exit 1
fi

echo "✅ docker-compose is available"

echo ""
echo "🎉 Setup validation completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Review your configuration in custom-certs.env"
echo "2. Start the services:"
echo "   docker-compose -f docker-compose.custom-certs.yml --env-file custom-certs.env up -d"
echo "3. Check the logs:"
echo "   docker-compose -f docker-compose.custom-certs.yml logs -f"
echo "4. Access your application:"
echo "   https://$DOMAIN"
echo ""
echo "🔧 Troubleshooting:"
echo "   - Check Traefik logs: docker-compose -f docker-compose.custom-certs.yml logs traefik"
echo "   - Verify certificate mounting: docker-compose -f docker-compose.custom-certs.yml exec traefik ls -la /etc/traefik/certs/"
echo "   - Test certificate: openssl s_client -connect $DOMAIN:443 -servername $DOMAIN"
echo ""
