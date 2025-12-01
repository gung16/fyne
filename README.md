# Fyne - Skincare Tracking Web App 🧴✨

A comprehensive Django-based skincare tracking application with a mobile-first design. Track your daily skin condition, manage your skincare routine, monitor UV exposure, and analyze your progress over time.

## 🎨 Features

### 1. **Daily Skin Checkpoint** 📸
- Rate 6 key skin metrics (0-100 scale):
  - Acne Level
  - Oil Level
  - Dark Spots
  - Redness
  - Hydration
  - Texture Quality
- Automatic overall score calculation
- Daily tracking with history

### 2. **UV & Environment Tracking** ☀️
- Log UV index exposure
- Track humidity levels
- Monitor pollution/air quality
- Location-based readings

### 3. **Product Management** 💧
- Maintain product catalog
- Track active skincare routine
- Categorize by product type (cleanser, toner, serum, moisturizer, sunscreen, etc.)
- Usage frequency tracking (AM/PM/Weekly)

### 4. **Ingredient Safety Checker** 🛡️
- Analyze product ingredients
- Risk level assessment (Safe/Caution/Avoid)
- Flag problematic ingredients
- Personalized safety notes

### 5. **Progress Tracking** 📊
- Visual progress timeline
- Trend analysis (Improving/Stable/Declining)
- 7-day and 30-day statistics
- AI-generated insights

### 6. **User Profile** 👤
- Skin type classification
- Personal skincare statistics
- Activity tracking

## 🎨 Design

### Color Palette
- Primary Dark: `#3E1E68` 
- Primary Medium: `#5D2F77`
- Secondary Pink: `#E45A92`
- Secondary Light: `#FFACAC`

### Mobile-First UI
- Maximum width: 430px (phone screen size)
- Black background on sides (desktop view)
- Bottom navigation bar
- Card-based interface
- Gradient accents

## 📊 Database Structure (ERD)

### Entities:
1. **UserProfile** - Extended user information
2. **DailyCheckpoint** - Daily skin scan results
3. **UVReading** - UV & environmental data
4. **SkincareProduct** - Product catalog
5. **ProductUsage** - User's routine tracker
6. **IngredientSafety** - Safety assessments
7. **ProgressRecord** - Aggregated progress data

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Virtual environment

### Installation

1. **Activate virtual environment**:
```bash
# Windows
.\venv\Scripts\activate

# Unix/Mac
source venv/bin/activate
```

2. **Install dependencies** (already done):
```bash
pip install -r requirements.txt
```

3. **Run migrations** (already done):
```bash
python manage.py migrate
```

4. **Start the server**:
```bash
python manage.py runserver
```

5. **Access the application**:
- Main app: http://localhost:8000
- Admin panel: http://localhost:8000/admin

### Default Credentials
- **Username**: `admin`
- **Password**: `admin123`

## 📱 Navigation

### Bottom Navigation Bar:
- 🏠 **Home** - Dashboard overview
- 📸 **Scan** - Daily checkpoint entry
- 🧪 **Products** - Product management
- 📈 **Progress** - Analytics & trends
- 👤 **Profile** - User settings

## 🔧 Tech Stack

- **Backend**: Django 5.2.8
- **Database**: SQLite (dev) / PostgreSQL (production)
- **Frontend**: HTML5, CSS3, JavaScript
- **Icons**: Font Awesome 6.4.0
- **Image Processing**: Pillow
- **Deployment Ready**: Gunicorn, Whitenoise, psycopg2

## 📂 Project Structure

```
fyne/
├── checkpoints/          # Checkpoint & UV tracking
│   ├── models.py         # DailyCheckpoint, UVReading
│   ├── views.py
│   └── urls.py
├── products/             # Product management
│   ├── models.py         # SkincareProduct, ProductUsage, IngredientSafety
│   ├── views.py
│   └── urls.py
├── progress/             # Progress analytics
│   ├── models.py         # ProgressRecord
│   ├── views.py
│   └── urls.py
├── users/                # User profiles
│   ├── models.py         # UserProfile
│   ├── views.py
│   └── urls.py
├── templates/            # HTML templates
│   ├── base.html         # Mobile-first base template
│   ├── dashboard.html
│   ├── login.html
│   ├── checkpoints/
│   ├── products/
│   ├── progress/
│   └── users/
├── static/
│   ├── css/
│   │   └── style.css     # Mobile-optimized styles
│   └── js/
└── fyne/                 # Project settings
    ├── settings.py
    ├── urls.py
    └── views.py
```

## 🎯 Key Features Explained

### Skin Score Calculation
The overall skin score is calculated as:
```
Overall = (
    (100 - acne_level) +
    (100 - oil_level) +
    (100 - dark_spots) +
    (100 - redness) +
    hydration_score +
    texture_score
) / 6
```

### Trend Analysis
Progress trends are determined by comparing the last 7 days:
- **Improving**: Score increased by > 5 points
- **Declining**: Score decreased by > 5 points
- **Stable**: Changes within ±5 points

### Ingredient Safety Logic
Flags risky ingredients:
- Alcohol
- Fragrance
- Parabens
- Sulfates

Risk levels:
- **Safe**: No flagged ingredients
- **Caution**: 1-2 flagged ingredients
- **Avoid**: 3+ flagged ingredients

## 🔐 Environment Variables

### Development (`.env`)
```
PRODUCTION=False
```

### Production (`.env.prod`)
```
DB_NAME=your_db_name
DB_HOST=your_db_host
DB_PORT=5432
DB_USER=your_db_user
DB_PASSWORD=your_db_password
SCHEMA=tutorial
PRODUCTION=True
```

## 📝 Admin Panel

Access Django admin at `/admin` to:
- Manage users and profiles
- View all checkpoints and readings
- Moderate product catalog
- Monitor progress records
- Review safety assessments

## 🚢 Deployment

Ready for deployment with:
- Environment-based configuration
- PostgreSQL support
- Static file handling (Whitenoise)
- Production-ready settings
- .gitignore configured

## 🤝 Contributing

This is a personal skincare tracking application. Future enhancements could include:
- AI-powered skin analysis from photos
- Product recommendations
- Weather API integration for UV data
- Export progress reports
- Social features (share routines)
- Multi-language support

## 📄 License

Personal project - All rights reserved

## 👨‍💻 Developer

Built with ❤️ by a professional MIT-trained engineer

---

**Happy Skincare Tracking! 🌟**
