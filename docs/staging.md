# Staging Environment Setup

This guide covers deploying the CryptoLib web application to a staging server for testing before production.

## Server Requirements

- **OS:** Ubuntu 22.04 LTS (or similar)
- **Python:** 3.11 or higher
- **Node.js:** 20 or higher
- **Database:** PostgreSQL 15 or higher
- **Web Server:** Nginx
- **Process Manager:** systemd
- **Memory:** Minimum 2GB RAM
- **Storage:** Minimum 10GB free space

## Prerequisites

- SSH access to the server
- Sudo privileges
- Domain name (optional, can use IP address)

## Step 1: System Setup

### 1.1 Update System Packages

```bash
sudo apt update
sudo apt upgrade -y
```

### 1.2 Install Required Packages

```bash
sudo apt install -y python3.11 python3.11-venv python3-pip \
    postgresql postgresql-contrib nginx git curl \
    build-essential libpq-dev
```

### 1.3 Install Node.js 20

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```

## Step 2: PostgreSQL Setup

### 2.1 Create Database and User

```bash
sudo -u postgres psql
```

In the PostgreSQL prompt:

```sql
CREATE DATABASE crypto_db;
CREATE USER crypto_user WITH PASSWORD 'your-secure-password';
ALTER ROLE crypto_user SET client_encoding TO 'utf8';
ALTER ROLE crypto_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE crypto_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE crypto_db TO crypto_user;
\q
```

## Step 3: Application Setup

### 3.1 Clone Repository

```bash
cd /var/www
sudo git clone <repository-url> cryptolib
sudo chown -R $USER:$USER /var/www/cryptolib
cd cryptolib
```

### 3.2 Backend Setup

```bash
cd backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3.3 Configure Environment

Create `.env` file:

```bash
nano .env
```

Add the following configuration:

```env
# Django Settings
DJANGO_SETTINGS_MODULE=core.settings.staging
SECRET_KEY=<generate-a-strong-secret-key>
DEBUG=False
ALLOWED_HOSTS=your-domain.com,your-server-ip

# Database
DB_NAME=crypto_db
DB_USER=crypto_user
DB_PASSWORD=your-secure-password
DB_HOST=localhost
DB_PORT=5432

# CORS
CORS_ALLOWED_ORIGINS=https://your-domain.com,http://your-server-ip

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=15
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
```

**Generate a strong SECRET_KEY:**
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 3.4 Run Migrations

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### 3.5 Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Build for production
npm run build
```

## Step 4: Gunicorn Setup

### 4.1 Create Gunicorn Socket

```bash
sudo nano /etc/systemd/system/cryptolib-gunicorn.socket
```

Add:

```ini
[Unit]
Description=Gunicorn socket for CryptoLib

[Socket]
ListenStream=/run/cryptolib-gunicorn.sock

[Install]
WantedBy=sockets.target
```

### 4.2 Create Gunicorn Service

```bash
sudo nano /etc/systemd/system/cryptolib-gunicorn.service
```

Add:

```ini
[Unit]
Description=Gunicorn daemon for CryptoLib
Requires=cryptolib-gunicorn.socket
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/cryptolib/backend
Environment="PATH=/var/www/cryptolib/backend/venv/bin"
ExecStart=/var/www/cryptolib/backend/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/run/cryptolib-gunicorn.sock \
          core.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 4.3 Set Permissions

```bash
sudo chown -R www-data:www-data /var/www/cryptolib
sudo chmod -R 755 /var/www/cryptolib
```

### 4.4 Start Gunicorn

```bash
sudo systemctl start cryptolib-gunicorn.socket
sudo systemctl enable cryptolib-gunicorn.socket
sudo systemctl start cryptolib-gunicorn.service
sudo systemctl enable cryptolib-gunicorn.service
```

Verify status:

```bash
sudo systemctl status cryptolib-gunicorn
```

## Step 5: Nginx Configuration

### 5.1 Create Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/cryptolib
```

Add:

```nginx
server {
    listen 80;
    server_name your-domain.com your-server-ip;

    # Frontend
    location / {
        root /var/www/cryptolib/frontend/build;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://unix:/run/cryptolib-gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Admin
    location /admin/ {
        proxy_pass http://unix:/run/cryptolib-gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files
    location /static/ {
        alias /var/www/cryptolib/backend/staticfiles/;
    }

    # PyScript demo
    location /pyscript/ {
        alias /var/www/cryptolib/pyscript/;
    }
}
```

### 5.2 Enable Site

```bash
sudo ln -s /etc/nginx/sites-available/cryptolib /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Step 6: SSL Certificate (Optional but Recommended)

### 6.1 Install Certbot

```bash
sudo apt install -y certbot python3-certbot-nginx
```

### 6.2 Obtain Certificate

```bash
sudo certbot --nginx -d your-domain.com
```

Follow the prompts. Certbot will automatically configure Nginx for HTTPS.

### 6.3 Auto-Renewal

```bash
sudo systemctl status certbot.timer
```

Test renewal:

```bash
sudo certbot renew --dry-run
```

## Step 7: Firewall Configuration

```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

## Testing the Deployment

1. **Frontend:** Navigate to `http://your-domain.com` or `http://your-server-ip`
2. **API:** Check `http://your-domain.com/api/`
3. **Admin:** Visit `http://your-domain.com/admin/`
4. **PyScript:** Visit `http://your-domain.com/pyscript/`

## Maintenance Commands

### Restart Services

```bash
sudo systemctl restart cryptolib-gunicorn
sudo systemctl restart nginx
```

### View Logs

```bash
# Gunicorn logs
sudo journalctl -u cryptolib-gunicorn -f

# Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Update Application

```bash
cd /var/www/cryptolib
git pull

# Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart cryptolib-gunicorn

# Frontend
cd ../frontend
npm install
npm run build
```

## Troubleshooting

### Gunicorn won't start

```bash
# Check logs
sudo journalctl -u cryptolib-gunicorn -n 50

# Check socket
sudo systemctl status cryptolib-gunicorn.socket
ls -la /run/cryptolib-gunicorn.sock
```

### Nginx 502 Bad Gateway

```bash
# Check if Gunicorn is running
sudo systemctl status cryptolib-gunicorn

# Check socket permissions
sudo chmod 666 /run/cryptolib-gunicorn.sock

# Restart services
sudo systemctl restart cryptolib-gunicorn
sudo systemctl restart nginx
```

### Database connection errors

```bash
# Test PostgreSQL connection
sudo -u postgres psql crypto_db

# Check .env file
cat /var/www/cryptolib/backend/.env

# Verify database user permissions
sudo -u postgres psql -c "\du"
```

## Next Steps

- Set up monitoring (e.g., Prometheus, Grafana)
- Configure automated backups
- Review [production.md](./production.md) for additional security measures
- Set up CI/CD pipeline for automated deployments
