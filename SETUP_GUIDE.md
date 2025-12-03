# 🚀 Quick Setup Guide

## Prerequisites
- Python 3.8+
- pip
- Git

## Installation Steps

### 1. Clone Repository
```bash
git clone https://github.com/rr0h/public-issue-tracker.git
cd public-issue-tracker
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment
```bash
cp .env.example .env
# Edit .env and set SECRET_KEY
```

### 5. Database Setup
```bash
python manage.py makemigrations accounts
python manage.py makemigrations issues
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
# Follow prompts to create admin account
```

### 7. Create Required Directories
```bash
mkdir -p static media media/issues media/profiles
```

### 8. Run Server
```bash
python manage.py runserver
```

### 9. Access Application
- **Main Site**: http://127.0.0.1:8000
- **Admin Panel**: http://127.0.0.1:8000/admin

## First Steps

### Create Test Users
1. Register as a citizen
2. Use admin panel to create worker accounts
3. Change user roles in admin panel

### Test the System
1. **As Citizen**: Report an issue with photo and location
2. **As Admin**: Access dashboard, view analytics
3. **As Admin**: Manage issue, update status, assign worker
4. **As Citizen**: Add comments, view updates
5. **Check Map**: View all issues on interactive map
6. **Resolved Gallery**: See before/after photos

## Common Issues

### Port Already in Use
```bash
python manage.py runserver 8080
```

### Static Files Not Loading
```bash
python manage.py collectstatic
```

### Database Errors
```bash
# Delete db.sqlite3 and migrations
rm db.sqlite3
rm -rf accounts/migrations/0*.py
rm -rf issues/migrations/0*.py

# Recreate
python manage.py makemigrations
python manage.py migrate
```

## Production Deployment

### Environment Variables
```bash
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:pass@host:port/dbname
```

### Static Files
```bash
python manage.py collectstatic --noinput
```

### Database
Use PostgreSQL for production:
```bash
pip install psycopg2-binary
```

## Features to Test

- ✅ User registration and login
- ✅ Issue creation with photos
- ✅ Location selection (manual/GPS)
- ✅ Issue filtering and search
- ✅ Interactive map view
- ✅ Admin dashboard with charts
- ✅ Status updates and timeline
- ✅ Comment system
- ✅ Before/after photos
- ✅ Resolved gallery
- ✅ Dark/light mode toggle
- ✅ AI duplicate detection
- ✅ AI priority suggestion
- ✅ Toxicity filtering

## Support

For issues or questions:
- GitHub Issues: https://github.com/rr0h/public-issue-tracker/issues
- Email: rajrohit9377@gmail.com

## Next Steps

1. Customize categories in `issues/models.py`
2. Add your Google Maps API key in `.env`
3. Configure email settings for notifications
4. Customize styling in templates
5. Add more AI features
6. Deploy to production

Happy tracking! 🎉
