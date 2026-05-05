# External API Guide

Industry Maintenance Platform provides secure external APIs for third-party integrations. These APIs are designed with a focus on security and access control.

## Security Features

### API Key Authentication
- Every request must include an `X-API-Key` header
- API Keys are securely generated and hashed in the database
- Support for automatic key expiration

### Rate Limiting
- Configurable limits per API Key
- Response headers with limit information
- Protection against abuse and DDoS attacks

### Multi-Tenant Isolation
- Each API Key is associated with a specific tenant
- Access only to authorized tenant data
- No possibility of cross-tenant access

### Audit Logging
- All requests are logged
- Tracking of IP, User-Agent, and endpoint
- API Key usage monitoring

### Multi-Deployment Support
- **Production**: https://imp.local/api
- **Custom Certificates**: https://yourdomain.com/api

## Configuration

### Creating API Keys

To create a new API Key, use the internal endpoint:

```bash
POST /api-keys
Content-Type: application/json
Authorization: Bearer <your-jwt-token>

{
  "name": "External System Integration",
  "scopes": ["read"],
  "rate_limit": "100/hour",
  "expires_at": "2026-12-31T23:59:59Z"
}
```

### Response
```json
{
  "id": "api-key-uuid",
  "name": "External System Integration",
  "key": "ind_abc123...", // Plain key (only during creation)
  "scopes": ["read"],
  "rate_limit": "100/hour",
  "expires_at": "2026-12-31T23:59:59Z",
  "created_at": "2026-04-20T10:00:00Z"
}
```

## API Usage

### Authentication

Always include the `X-API-Key` header in requests:

```bash
curl -H "X-API-Key: ind_abc123..." \
     https://api.industry-maintenance-platform.com/external/v1/assets
```

### Available Endpoints

#### API Information
```http
GET /external/v1/info
```

#### Verify API Key
```http
GET /external/v1/auth/verify
```

#### List Assets
```http
GET /external/v1/assets?skip=0&limit=100&status_id=uuid&site_id=uuid
```

#### Specific Asset
```http
GET /external/v1/assets/{asset_id}
```

#### Asset Statistics
```http
GET /external/v1/assets/stats/overview
```

#### High-Risk Assets
```http
GET /external/v1/assets/risk/high
```

#### Health Check
```http
GET /external/v1/health
```

## API Key Management

### Using Python Script

```bash
# Enter the container
docker-compose exec backend bash

# Generate basic API Key (read-only)
python generate_api_key.py create "Test API" admin@example.com

# Generate API Key with specific scopes
python generate_api_key.py create "Read Only" admin@example.com read 50/hour 30

# Generate API Key with all scopes
python generate_api_key.py create "Full Access" admin@example.com "read,write" 100/hour 365

# List all API Keys for a user
python generate_api_key.py list admin@example.com
```

### API Key Parameters

| Parameter | Description | Default | Examples |
|-----------|-------------|---------|----------|
| `name` | Descriptive name | - | "Test API", "Read Only" |
| `scopes` | Permissions | `["read"]` | `["read"]`, `["read", "write"]` |
| `rate_limit` | Request limit | `"100/hour"` | `"50/hour"`, `"10/minute"` |
| `expires_days` | Duration in days | `365` | `30`, `90`, `365` |

### Available Scopes

| Scope | Description | Endpoints |
|-------|-------------|-----------|
| `read` | Asset read access | `GET /external/v1/assets/*` |
| `write` | Asset write access | `POST/PUT/DELETE /external/v1/assets/*` |
| `stats` | Statistics access | `GET /external/v1/assets/stats/*` |
| `risk` | Risk assessment | `GET /external/v1/assets/risk/*` |

## Usage Examples

### Verify API Key
```bash
curl -X GET "http://localhost:8000/external/v1/auth/verify" \
  -H "X-API-Key: YOUR_API_KEY_HERE"
```

### List Assets
```bash
curl -X GET "http://localhost:8000/external/v1/assets" \
  -H "X-API-Key: YOUR_API_KEY_HERE"
```

### Get Specific Asset
```bash
curl -X GET "http://localhost:8000/external/v1/assets/ASSET_ID" \
  -H "X-API-Key: YOUR_API_KEY_HERE"
```

### Asset Statistics
```bash
curl -X GET "http://localhost:8000/external/v1/assets/stats/overview" \
  -H "X-API-Key: YOUR_API_KEY_HERE"
```

### High-Risk Assets
```bash
curl -X GET "http://localhost:8000/external/v1/assets/risk/high" \
  -H "X-API-Key: YOUR_API_KEY_HERE"
```

## Response Format

### Success Response
```json
{
  "success": true,
  "data": [...],
  "total": 100,
  "page": 1,
  "size": 10
}
```

### Error Response
```json
{
  "success": false,
  "error": "INVALID_API_KEY",
  "error_code": "AUTH_001",
  "message": "Invalid or expired API key"
}
```

## Error Codes

| Code | Description |
|------|-------------|
| `AUTH_001` | Invalid or expired API key |
| `AUTH_002` | Insufficient permissions |
| `RATE_001` | Rate limit exceeded |
| `TENANT_001` | Tenant access denied |
| `VAL_001` | Invalid request parameters |

## Rate Limiting

Rate limits are enforced per API Key:

- **Default**: 100 requests/hour
- **Strict**: 10 requests/minute for sensitive operations
- **Headers**: Include current usage information

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

## Best Practices

### Security
1. **Secure Storage**: Store API keys securely, never in client-side code
2. **Key Rotation**: Regularly rotate API keys
3. **Minimal Permissions**: Use the minimum required scopes
4. **HTTPS**: Always use HTTPS in production

### Performance
1. **Caching**: Cache static data like asset types
2. **Pagination**: Use pagination for large datasets
3. **Rate Limits**: Respect rate limits and implement backoff
4. **Connection Pooling**: Reuse connections when possible

### Error Handling
1. **Status Codes**: Check HTTP status codes
2. **Error Messages**: Handle error responses appropriately
3. **Retry Logic**: Implement retry logic for transient errors
4. **Logging**: Log errors for debugging

## Monitoring and Logging

### Audit Logs
All external API requests are logged with:
- API Key ID
- IP address
- User-Agent
- Endpoint accessed
- Response status
- Timestamp

### Usage Monitoring
Monitor API usage through:
- Rate limit headers
- Audit log analysis
- Dashboard statistics

## Troubleshooting

### Common Issues

#### Invalid API Key
```json
{
  "error": "INVALID_API_KEY",
  "message": "The provided API key is invalid or expired"
}
```
**Solution**: Verify the API key is correct and not expired

#### Rate Limit Exceeded
```json
{
  "error": "RATE_LIMIT_EXCEEDED",
  "message": "Rate limit exceeded. Try again later."
}
```
**Solution**: Implement exponential backoff and respect rate limits

#### Insufficient Permissions
```json
{
  "error": "INSUFFICIENT_PERMISSIONS",
  "message": "API key does not have required permissions"
}
```
**Solution**: Request additional scopes for the API key

## Support

For external API support:
1. Check the API documentation
2. Verify API key permissions
3. Review rate limiting settings
4. Check audit logs for request details
5. Contact system administrator for access issues 