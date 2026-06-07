# Production Deployment Guide

This guide covers best practices for deploying the CryptoLib web application to a production environment.

## Overview

Production deployment builds upon the staging setup with additional security, monitoring, and reliability features.

## Prerequisites

Complete all steps from [staging.md](./staging.md), then apply the additional production hardening steps below.

## Production Checklist

### Security Hardening

#### 1. Django Settings

Ensure `backend/core/settings/production.py` is properly configured:

```python
# Set via environment variable
DJANGO_SETTINGS_MODULE=core.settings.production

# Must be False in production
DEBUG = False

# Specific domains only (no wildcards)
ALLOWED_HOSTS = ['cryptolib.example.com', 'www.cryptolib.example.com']

# Force HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Additional security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

#### 2. Strong SECRET_KEY

Generate a cryptographically strong secret key:

```bash
python -c 'import secrets; print(secrets.token_urlsafe(50))'
```

Store in `.env` file, never commit to version control.

#### 3. Database Security

**Strong password policy:**
```bash
# Use a password manager to generate 32+ character password
DB_PASSWORD=$(openssl rand -base64 32)
```

**Restrict PostgreSQL access:**

Edit `/etc/postgresql/15/main/pg_hba.conf`:

```
# Only allow local connections
local   crypto_db    crypto_user                     md5
host    crypto_db    crypto_user    127.0.0.1/32     md5
```

Restart PostgreSQL:
```bash
sudo systemctl restart postgresql
```

#### 4. Firewall Configuration

```bash
# Reset and configure UFW
sudo ufw --force reset
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

#### 5. Fail2Ban

Protect against brute force attacks:

```bash
sudo apt install -y fail2ban

# Create config
sudo nano /etc/fail2ban/jail.local
```

Add:

```ini
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true

[nginx-http-auth]
enabled = true

[nginx-noscript]
enabled = true

[nginx-badbots]
enabled = true
```

Start Fail2Ban:

```bash
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

## Environment Variables Management

### Production .env File

Never commit `.env` to version control. Use a secure method to transfer:

```bash
# Example: Use scp with proper permissions
scp .env user@production-server:/var/www/cryptolib/backend/.env
ssh user@production-server 'chmod 600 /var/www/cryptolib/backend/.env'
```

### Environment Variables Template

```env
# Django
DJANGO_SETTINGS_MODULE=core.settings.production
SECRET_KEY=<50+ character random string>
DEBUG=False
ALLOWED_HOSTS=cryptolib.example.com,www.cryptolib.example.com

# Database
DB_NAME=crypto_db
DB_USER=crypto_user
DB_PASSWORD=<32+ character random string>
DB_HOST=localhost
DB_PORT=5432

# CORS
CORS_ALLOWED_ORIGINS=https://cryptolib.example.com,https://www.cryptolib.example.com

# JWT
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=15
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
```

## Database Backups

### Automated Daily Backups

Create backup script:

```bash
sudo nano /usr/local/bin/backup-cryptolib-db.sh
```

Add:

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/cryptolib"
DB_NAME="crypto_db"
DATE=$(date +%Y%m%d_%H%M%S)
FILENAME="cryptolib_backup_${DATE}.sql.gz"

mkdir -p $BACKUP_DIR
pg_dump $DB_NAME | gzip > "${BACKUP_DIR}/${FILENAME}"

# Keep only last 30 days of backups
find $BACKUP_DIR -type f -mtime +30 -delete

# Optional: Upload to S3 or remote backup
# aws s3 cp "${BACKUP_DIR}/${FILENAME}" s3://your-backup-bucket/
```

Make executable:

```bash
sudo chmod +x /usr/local/bin/backup-cryptolib-db.sh
```

Create cron job:

```bash
sudo crontab -e
```

Add:

```
0 2 * * * /usr/local/bin/backup-cryptolib-db.sh
```

### Restore from Backup

```bash
gunzip -c /var/backups/cryptolib/cryptolib_backup_YYYYMMDD_HHMMSS.sql.gz | \
    sudo -u postgres psql crypto_db
```

## Monitoring

### Application Monitoring

#### Install Prometheus and Grafana (Optional)

```bash
# Prometheus
sudo apt install -y prometheus

# Grafana
sudo apt-get install -y software-properties-common
sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
sudo apt-get update
sudo apt-get install grafana
```

### Log Monitoring

#### Centralized Logging

```bash
# Install Logrotate for log management
sudo apt install -y logrotate
```

Create logrotate config:

```bash
sudo nano /etc/logrotate.d/cryptolib
```

Add:

```
/var/www/cryptolib/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
}
```

### Uptime Monitoring

Use external services like:
- UptimeRobot (https://uptimerobot.com/)
- Pingdom (https://www.pingdom.com/)
- StatusCake (https://www.statuscake.com/)

Set up alerts for:
- Website downtime
- API response time > 2s
- SSL certificate expiration
- Disk space > 80%

## Performance Optimization

### Database Optimization

```sql
-- Create indexes for frequently queried fields
CREATE INDEX idx_auth_user_username ON auth_user(username);
CREATE INDEX idx_auth_user_email ON auth_user(email);
```

### Nginx Caching

Update Nginx config:

```nginx
# Add to server block
location /static/ {
    alias /var/www/cryptolib/backend/staticfiles/;
    expires 30d;
    add_header Cache-Control "public, immutable";
}

location / {
    root /var/www/cryptolib/frontend/build;
    try_files $uri $uri/ /index.html;
    
    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### Gunicorn Workers

Optimize worker count based on CPU cores:

```bash
# Formula: (2 x CPU cores) + 1
# For 2 cores: 5 workers
sudo nano /etc/systemd/system/cryptolib-gunicorn.service
```

Update:

```ini
ExecStart=/var/www/cryptolib/backend/venv/bin/gunicorn \
          --workers 5 \
          --worker-class gthread \
          --threads 2 \
          --bind unix:/run/cryptolib-gunicorn.sock \
          --access-logfile /var/log/gunicorn/access.log \
          --error-logfile /var/log/gunicorn/error.log \
          core.wsgi:application
```

## Docker Deployment (Alternative)

### Dockerfile (Backend)

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
```

### docker-compose.yml

Create in project root:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: crypto_db
      POSTGRES_USER: crypto_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - cryptolib

  backend:
    build: ./backend
    command: gunicorn --bind 0.0.0.0:8000 core.wsgi:application
    volumes:
      - ./backend:/app
      - static_volume:/app/staticfiles
    environment:
      - DJANGO_SETTINGS_MODULE=core.settings.production
      - SECRET_KEY=${SECRET_KEY}
      - DB_NAME=crypto_db
      - DB_USER=crypto_user
      - DB_PASSWORD=${DB_PASSWORD}
      - DB_HOST=db
      - DB_PORT=5432
    depends_on:
      - db
    networks:
      - cryptolib

  frontend:
    build: ./frontend
    volumes:
      - ./frontend/build:/app/build
    networks:
      - cryptolib

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/static
      - ./frontend/build:/var/www/frontend
    depends_on:
      - backend
    networks:
      - cryptolib

volumes:
  postgres_data:
  static_volume:

networks:
  cryptolib:
```

### Deploy with Docker

```bash
# Build and start
docker-compose up -d

# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Collect static files
docker-compose exec backend python manage.py collectstatic --noinput
```

## SSL/TLS Best Practices

### Certificate Monitoring

```bash
# Check certificate expiration
echo | openssl s_client -servername cryptolib.example.com \
    -connect cryptolib.example.com:443 2>/dev/null | \
    openssl x509 -noout -dates
```

### Strong SSL Configuration

Update Nginx SSL settings:

```nginx
# Modern SSL configuration
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
ssl_prefer_server_ciphers off;

# OCSP Stapling
ssl_stapling on;
ssl_stapling_verify on;
resolver 8.8.8.8 8.8.4.4 valid=300s;
resolver_timeout 5s;
```

## Health Checks

Create health check endpoint in Django:

```python
# backend/api/views.py
from django.http import JsonResponse
from django.db import connection

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    try:
        # Check database
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({'status': 'healthy'})
    except Exception as e:
        return JsonResponse({'status': 'unhealthy', 'error': str(e)}, status=503)
```

Add to urls.py:

```python
path('health/', views.health_check, name='health_check'),
```

## Incident Response Plan

1. **Define contacts:** Maintain list of on-call personnel
2. **Monitoring alerts:** Set up PagerDuty or similar
3. **Rollback procedure:** Document how to revert to previous version
4. **Communication plan:** Who to notify and when
5. **Post-mortem:** Template for incident analysis

## Compliance and Legal

- **GDPR:** If serving EU users, ensure compliance
- **Data retention:** Define and implement policies
- **Privacy policy:** Have legal review
- **Terms of service:** Clearly defined
- **Cookie consent:** If using analytics

## Regular Maintenance Tasks

### Weekly
- Review error logs
- Check disk space
- Monitor SSL certificate expiration
- Review failed login attempts

### Monthly
- Update dependencies (test in staging first)
- Review and rotate access credentials
- Audit user accounts
- Database optimization and vacuum

### Quarterly
- Security audit
- Performance testing
- Disaster recovery drill
- Update documentation

## Resources

- Django Security: https://docs.djangoproject.com/en/4.2/topics/security/
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- Mozilla SSL Config: https://ssl-config.mozilla.org/

## Support

For issues or questions:
- Check logs: `sudo journalctl -u cryptolib-gunicorn -f`
- Review documentation
- Contact development team
