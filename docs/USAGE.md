# API Usage Guide

## Authentication

Currently, this API does not require authentication. All endpoints are publicly accessible.

## Rate Limiting

- Default limit: 60 requests per minute
- Configure via `RATE_LIMIT_PER_MINUTE` environment variable

## Response Format

All API responses follow a consistent format:

### Success Response
```json
{
  "code": 200,
  "status": "success",
  "message": "Request processed successfully",
  "data": { }
}
```

### Error Response
```json
{
  "error": "Error Type",
  "message": "Error description",
  "details": { }
}
```

## Common Query Parameters

### Language Support

Most endpoints support the `lang` parameter:

- `en` - English (default)
- `id` - Indonesian
- `zh` - Chinese
- And more...

Example:
```
GET /api/hero-list/?lang=id
```

### Pagination

Endpoints that return lists support pagination:

- `size`: Number of items per page (default: 20)
- `index`: Page index starting from 1 (default: 1)

Example:
```
GET /api/hero-rank/?size=50&index=2
```

## Endpoint Examples

### Get Hero List

```bash
curl -X GET "https://mlbb-stats.ridwaanhall.com/api/hero-list/?lang=en"
```

### Get Hero Rankings

```bash
curl -X GET "https://mlbb-stats.ridwaanhall.com/api/hero-rank/?days=7&rank=mythic&sort_field=win_rate&sort_order=desc"
```

### Calculate Win Rate

```bash
curl -X GET "https://mlbb-stats.ridwaanhall.com/api/win-rate/?match-now=100&wr-now=50&wr-future=75"
```

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid parameters |
| 404 | Not Found - Endpoint doesn't exist |
| 500 | Internal Server Error |
| 502 | Bad Gateway - External API error |
| 503 | Service Unavailable - Maintenance mode |

## Best Practices

1. **Cache responses** when possible to reduce API calls
2. **Handle errors gracefully** with appropriate retries
3. **Use pagination** for large datasets
4. **Respect rate limits** to avoid throttling
5. **Monitor API status** via `/health` endpoint

## Support

For issues or questions:
- GitHub Issues: https://github.com/ridwaanhall/api-mobilelegends/issues
- Sponsor: https://github.com/sponsors/ridwaanhall
