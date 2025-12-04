# 🚀 Deployment Guide

## Production Deployment Options

### Option 1: Heroku (Recommended for Beginners)

#### Prerequisites
- Heroku account
- Heroku CLI installed

#### Steps
```bash
# 1. Login to Heroku
heroku login

# 2. Create Heroku app
heroku create your-app-name

# 3. Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# 4. Set environment variables
heroku config:set SECRET_KEY='your-secret-key'
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS='your-app-name.herokuapp.com'

# 5. Deploy
git push heroku main

# 6. Run migrations
heroku run python manage.py migrate

# 7. Create superuser
heroku run python manage.py createsuperuser

# 8. Collect static files
heroku run python manage.py collectstatic --noinput

# 9. Open app
heroku open
```

#### Additional Configuration
Create `Procfile`:
```
web: gunicorn issue_tracker.wsgi
```

Create `runtime.txt`:
```
python-3.11.0
```

---

### Option 2: Railway

#### Steps
1. Visit https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose `public-issue-tracker`
5. Add PostgreSQL database
6. Set environment variables
7. Deploy automatically

#### Environment Variables
```
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=postgresql://... (auto-set by Railway)
ALLOWED_HOSTS=your-app.railway.app
```

---

### Option 3: DigitalOcean App Platform

#### Steps
1. Visit DigitalOcean App Platform
2. Create new app from GitHub
3. Select repository
4. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `gunicorn issue_tracker.wsgi`
5. Add PostgreSQL database
6. Set environment variables
7. Deploy

---

### Option 4: AWS EC2

#### Prerequisites
- AWS account
- EC2 instance (Ubuntu 20.04+)

#### Steps
```bash
# 1. SSH into EC2
ssh -i your-key.pem ubuntu@your-ec2-ip

# 2. Update system
sudo apt update && sudo apt upgrade -y

# 3. Install Python and dependencies
sudo apt install python3-pip python3-venv nginx -y

# 4. Clone repository
git clone https://github.com/rr0h/public-issue-tracker.git
cd public-issue-tracker

# 5. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 6. Install dependencies
pip install -r requirements.txt
pip install gunicorn

# 7. Setup environment
cp .env.example .env
nano .env  # Edit configuration

# 8. Run migrations
python manage.py migrate
python manage.py collectstatic

# 9. Create superuser
python manage.py createsuperuser

# 10. Configure Gunicorn
sudo nano /etc/systemd/system/gunicorn.service
```

Gunicorn service file:
```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/public-issue-tracker
ExecStart=/home/ubuntu/public-issue-tracker/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/home/ubuntu/public-issue-tracker/gunicorn.sock \
          issue_tracker.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# 11. Start Gunicorn
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

# 12. Configure Nginx
sudo nano /etc/nginx/sites-available/issue_tracker
```

Nginx configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/ubuntu/public-issue-tracker;
    }
    
    location /media/ {
        root /home/ubuntu/public-issue-tracker;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/public-issue-tracker/gunicorn.sock;
    }
}
```

```bash
# 13. Enable Nginx site
sudo ln -s /etc/nginx/sites-available/issue_tracker /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx

# 14. Configure firewall
sudo ufw allow 'Nginx Full'
```

---

### Option 5: Docker Deployment

#### Create Dockerfile
```dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "issue_tracker.wsgi:application"]
```

#### Create docker-compose.yml
```yaml
version: '3.8'

services:
  db:
    image: postgres:14
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=issue_tracker
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres

  web:
    build: .
    command: gunicorn issue_tracker.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

#### Deploy with Docker
```bash
# Build and run
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

---

## Production Checklist

### Security
- [ ] Set `DEBUG=False`
- [ ] Generate strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Enable HTTPS/SSL
- [ ] Set secure cookies
- [ ] Configure CORS properly
- [ ] Use environment variables

### Database
- [ ] Use PostgreSQL (not SQLite)
- [ ] Configure database backups
- [ ] Set up connection pooling
- [ ] Optimize database queries

### Static Files
- [ ] Run `collectstatic`
- [ ] Configure CDN (optional)
- [ ] Enable gzip compression
- [ ] Set cache headers

### Media Files
- [ ] Configure media storage (S3, etc.)
- [ ] Set file upload limits
- [ ] Enable image optimization

### Performance
- [ ] Enable caching (Redis/Memcached)
- [ ] Configure database indexes
- [ ] Use connection pooling
- [ ] Enable query optimization

### Monitoring
- [ ] Set up error tracking (Sentry)
- [ ] Configure logging
- [ ] Set up uptime monitoring
- [ ] Enable performance monitoring

### Email
- [ ] Configure SMTP settings
- [ ] Set up email templates
- [ ] Test email delivery

### Backup
- [ ] Database backups
- [ ] Media file backups
- [ ] Code repository backups

---

## Environment Variables for Production

```bash
# Django
SECRET_KEY=your-production-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Google Maps (Optional)
GOOGLE_MAPS_API_KEY=your-api-key

# AWS S3 (Optional)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1

# Sentry (Optional)
SENTRY_DSN=your-sentry-dsn
```

---

## SSL/HTTPS Setup

### Using Let's Encrypt (Free)
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

---

## Performance Optimization

### Enable Caching
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### Database Connection Pooling
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'connect_timeout': 10,
            'options': '-c statement_timeout=30000',
        },
        'CONN_MAX_AGE': 600,
    }
}
```

---

## Monitoring Setup

### Sentry Integration
```bash
pip install sentry-sdk
```

```python
# settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
)
```

---

## Troubleshooting

### Static files not loading
```bash
python manage.py collectstatic --clear
python manage.py collectstatic --noinput
```

### Database connection errors
- Check DATABASE_URL
- Verify database credentials
- Ensure database is running

### 502 Bad Gateway
- Check Gunicorn is running
- Verify Nginx configuration
- Check application logs

### Permission errors
```bash
sudo chown -R www-data:www-data /path/to/app
sudo chmod -R 755 /path/to/app
```

---

## Maintenance

### Update application
```bash
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

### Database backup
```bash
# PostgreSQL
pg_dump dbname > backup.sql

# Restore
psql dbname < backup.sql
```

---

## Support

For deployment issues:
- Check logs: `heroku logs --tail` or `sudo journalctl -u gunicorn`
- GitHub Issues: https://github.com/rr0h/public-issue-tracker/issues
- Email: rajrohit9377@gmail.com

---

**Happy Deploying! 🚀**
