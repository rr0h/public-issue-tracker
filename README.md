# 🏙️ Public Issue Tracker for Local Community

A comprehensive civic-tech platform built with Django that enables citizens to report local community issues (potholes, garbage, broken street lights, water leakage, etc.) and allows authorities to track, manage, and resolve them efficiently.

![Django](https://img.shields.io/badge/Django-4.2.7-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

### 🎯 Core Features
- **User Authentication**: Register, login, logout with role-based access (Citizen, Admin, Worker)
- **Issue Reporting**: Citizens can report issues with photos, location, and urgency level
- **Interactive Map**: Leaflet.js powered map showing all issues with color-coded status markers
- **Status Workflow**: Complete lifecycle from Pending → Reviewed → Assigned → In Progress → Resolved/Rejected
- **Before & After Photos**: Visual proof of issue resolution
- **Comment System**: Discussion threads with AI-powered toxicity filtering
- **Admin Dashboard**: Comprehensive analytics with Chart.js visualizations
- **Resolved Gallery**: Public showcase of completed work

### 🤖 AI-Powered Features
1. **Duplicate Issue Detection**: TF-IDF based similarity detection to identify duplicate reports
2. **Location Proximity Check**: Haversine formula to detect nearby similar issues
3. **Priority Classifier**: NLP-based automatic priority suggestion
4. **Toxicity Filter**: Automatic detection and filtering of inappropriate comments

### 📊 Admin Capabilities
- Real-time dashboard with statistics
- Issue assignment to workers
- Status updates with timeline
- Performance metrics (avg resolution time, resolution rate)
- Category and status analytics with charts
- Bulk issue management

### 🎨 UI/UX Features
- **Tailwind CSS**: Modern, responsive design
- **Dark/Light Mode**: Toggle between themes
- **Status Badges**: Color-coded visual indicators
- **Smooth Animations**: Hover effects and transitions
- **Mobile Responsive**: Works on all devices
- **Accessibility**: WCAG compliant

## 🛠️ Tech Stack

- **Backend**: Django 4.2.7, Python 3.8+
- **Frontend**: Tailwind CSS, JavaScript
- **Database**: SQLite (development), PostgreSQL ready
- **Maps**: Leaflet.js / Google Maps API
- **Charts**: Chart.js
- **AI/ML**: scikit-learn, TF-IDF
- **Icons**: Font Awesome 6

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone the Repository
```bash
git clone https://github.com/rr0h/public-issue-tracker.git
cd public-issue-tracker
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Environment Configuration
```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your configuration
# Minimum required: SECRET_KEY
```

### Step 5: Database Setup
```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser
```

### Step 6: Create Static Directories
```bash
mkdir -p static media
```

### Step 7: Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser!

## 📁 Project Structure

```
public-issue-tracker/
├── issue_tracker/          # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/               # User authentication app
│   ├── models.py          # Custom User model
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── issues/                 # Core issues app
│   ├── models.py          # Issue, IssueUpdate, Comment models
│   ├── views.py           # All views
│   ├── forms.py           # Forms
│   ├── ai_utils.py        # AI features
│   ├── admin.py
│   └── urls.py
├── templates/              # HTML templates
│   ├── base.html
│   ├── accounts/
│   └── issues/
├── static/                 # Static files (CSS, JS, images)
├── media/                  # User uploaded files
├── requirements.txt
├── manage.py
└── README.md
```

## 🗄️ Database Models

### User Model
- Custom user with roles (citizen/admin/worker)
- Profile information (phone, address, profile picture)

### Issue Model
- Title, category, description
- Location (latitude, longitude, address)
- Photos (before/after)
- Status workflow
- Urgency level
- Assignment tracking

### IssueUpdate Model
- Status change history
- Comments and updates
- Assignment records
- Resolution photos

### Comment Model
- User comments
- Toxicity detection flag
- Timestamps

## 🎯 Usage Guide

### For Citizens
1. **Register**: Create an account
2. **Report Issue**: Click "Report Issue", fill form with details, photos, and location
3. **Track Progress**: View your issues and status updates
4. **Comment**: Engage in discussions about issues

### For Admins
1. **Dashboard**: Access admin dashboard for overview
2. **Manage Issues**: Update status, assign to workers
3. **Add Updates**: Provide comments and upload resolution photos
4. **Analytics**: View charts and performance metrics

### For Workers
1. **View Assigned Issues**: See issues assigned to you
2. **Update Progress**: Change status as work progresses
3. **Upload Photos**: Add after photos when resolved

## 🔐 User Roles

| Role | Permissions |
|------|-------------|
| **Citizen** | Report issues, comment, view own issues |
| **Admin** | All citizen permissions + manage all issues, assign workers, access dashboard |
| **Worker** | All citizen permissions + update assigned issues |

## 🚀 Features Walkthrough

### 1. Issue Reporting
- Upload photos (before state)
- Add location (manual or GPS)
- Select category and urgency
- AI suggests priority based on description

### 2. Duplicate Detection
- Automatically checks for similar issues
- Uses text similarity (TF-IDF)
- Checks location proximity
- Warns user if duplicate found

### 3. Interactive Map
- Color-coded markers by status
- Click markers for issue details
- Filter by category/status
- Responsive and mobile-friendly

### 4. Admin Dashboard
- Total issues count
- Status breakdown
- Category distribution charts
- Average resolution time
- Recent issues table

### 5. Resolved Gallery
- Before/after photo comparison
- Resolution date and time
- Category and location info
- Public transparency

## 🧪 Testing

Run Django tests:
```bash
python manage.py test
```

Test coverage includes:
- Issue creation
- Status updates
- User authentication
- AI utilities
- Map functionality

## 🌐 API Endpoints

RESTful API available at `/api/`:

- `GET /api/issues/` - List all issues
- `GET /api/issues/<uuid>/` - Issue details
- `GET /api/stats/` - Statistics

## 📱 Screenshots

### Home Page
Modern landing page with statistics and recent issues

### Issue List
Filterable grid view with category and status badges

### Issue Detail
Complete issue information with timeline and comments

### Admin Dashboard
Analytics dashboard with charts and metrics

### Map View
Interactive map with color-coded issue markers

### Resolved Gallery
Before/after photo showcase

## 🔧 Configuration

### Google Maps API (Optional)
Add to `.env`:
```
GOOGLE_MAPS_API_KEY=your_api_key_here
```

### Email Configuration
For password reset functionality:
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG=False` in settings
- [ ] Configure proper `SECRET_KEY`
- [ ] Set up PostgreSQL database
- [ ] Configure static files serving
- [ ] Set up media files storage
- [ ] Configure email backend
- [ ] Set up HTTPS
- [ ] Configure allowed hosts

### Deploy to Heroku
```bash
# Install Heroku CLI
heroku create your-app-name
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- **Rohit Raj** - Initial work - [rr0h](https://github.com/rr0h)

## 🙏 Acknowledgments

- Django community for excellent documentation
- Tailwind CSS for beautiful styling
- Leaflet.js for interactive maps
- Chart.js for data visualization
- Font Awesome for icons

## 📞 Support

For support, email rajrohit9377@gmail.com or open an issue on GitHub.

## 🗺️ Roadmap

- [ ] Mobile app (React Native)
- [ ] Real-time notifications
- [ ] SMS alerts
- [ ] Multi-language support
- [ ] Advanced analytics
- [ ] Integration with municipal systems
- [ ] Voting system for issue priority
- [ ] Gamification and rewards

## ⭐ Star History

If you find this project useful, please consider giving it a star!

---

**Built with ❤️ for better communities**
