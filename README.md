# NewsPortal - Modern Django News Portal

A production-ready, scalable, SEO-optimized News Portal built with Django 5+ and modern web technologies.

## Tech Stack

- **Backend**: Python 3.12+, Django 5+, Django REST Framework
- **Database**: PostgreSQL
- **Frontend**: Tailwind CSS, Alpine.js, HTMX
- **Editor**: CKEditor 5
- **Cache**: Redis (optional)
- **Task Queue**: Celery (optional)

## Features

### User Management
- Registration with email verification
- Login/Logout
- Password reset
- Profile management with avatar
- Role-based access (Guest, User, Journalist, Editor, Admin)

### Content Management
- Rich text editor (CKEditor 5)
- Featured images with galleries
- Categories and tags
- Draft/published/archived states
- Scheduled publishing
- Reading time estimation
- View counter, likes, bookmarks

### News Features
- Breaking news slider
- Trending articles
- Editor's picks
- Featured articles
- Most viewed
- Category pages with pagination
- Author pages with statistics

### User Dashboard
- Profile editing
- Bookmarks management
- Reading history
- Comments management
- Notification preferences

### Author Dashboard
- Article CRUD
- Draft management
- Statistics and analytics

### Admin Dashboard
- User management
- Article moderation
- Comment moderation
- Category management
- Newsletter management
- Contact messages
- Website settings
- Analytics overview

### Additional Features
- AJAX live search
- Newsletter subscription
- Social media sharing
- Print articles
- Dark/Light mode
- Responsive design
- SEO optimization
- XML Sitemap
- robots.txt
- Open Graph / Twitter Cards
- JSON-LD structured data
- Canonical URLs

## Installation

### Prerequisites
- Python 3.12+
- PostgreSQL
- Node.js (for Tailwind CSS)
- Redis (optional)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/newsportal.git
cd newsportal
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
cp .env.example .env
# Edit .env with your database credentials and settings
```

### Step 5: Database Setup
```bash
python manage.py migrate
python manage.py seed_data
```

### Step 6: Create Superuser (if not using seed)
```bash
python manage.py createsuperuser
```

### Step 7: Run Development Server
```bash
python manage.py runserver
```

### Step 8: Build Tailwind CSS (optional)
```bash
npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch
```

## Default Accounts (after seed)
| Username    | Password        | Role     |
|-------------|-----------------|----------|
| admin       | admin123        | Admin    |
| journalist  | journalist123   | Journalist |

## API Endpoints

| Method | Endpoint                     | Description          |
|--------|------------------------------|----------------------|
| POST   | /api/auth/login/             | Obtain JWT token     |
| POST   | /api/auth/register/          | Register user        |
| GET    | /api/articles/               | List articles        |
| GET    | /api/articles/{id}/          | Article detail       |
| POST   | /api/articles/{id}/like/     | Like article         |
| POST   | /api/articles/{id}/bookmark/ | Bookmark article     |
| GET    | /api/categories/             | List categories      |
| GET    | /api/comments/               | List comments        |
| GET    | /api/search/?q=query         | Search articles      |
| GET    | /api/trending/               | Trending articles    |
| GET    | /api/breaking/               | Breaking news        |

## Project Structure
```
newsportal/
├── accounts/           # Authentication & user management
├── advertisements/     # Ad management
├── api/                # REST API
├── comments/           # Comments system
├── core/               # Core models & utilities
├── dashboard/          # Author & Admin dashboards
├── news/               # Main news application
├── newsletter/         # Newsletter subscription
├── notifications/      # Notification system
├── templates/          # HTML templates
├── static/             # Static assets
├── media/              # User uploaded files
└── news_portal/        # Project configuration
```

## License
MIT License
