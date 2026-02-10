# URL Shortener with Expiry and Analytics

A Python-based URL shortener built with FastAPI and SQLite.  
It supports link expiration and tracks usage analytics.

## Features
- Shorten URLs with unique identifiers
- Set custom expiry (default: 24 hours)
- Redirect only if not expired
- Track access count, timestamps, and IP addresses
- REST API endpoints

## Endpoints
- `POST /shorten` → Create a shortened URL
- `GET /<short_url>` → Redirect if valid
- `GET /analytics/<short_url>` → View analytics


