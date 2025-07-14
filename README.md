# medata: a medical research data management system

This is a medical research data management system (medata) for Kawasaki disease research. The application is a full-stack web application with a Django REST API backend and Vue.js frontend.

## Architecture

### Backend (Django)
- **Framework**: Django 4.0+ with Django REST Framework
- **Database**: SQLite3 for development/production
- **Main App**: `apps/kawasaki` contains all medical data models and APIs
- **Key Models**: Patient, BloodTest, LiverFunction, Echocardiography, InfectiousTest, Samples, CustomTest
- **Authentication**: Token-based authentication via DRF
- **Special Features**: Implements optimistic locking for data integrity

### Frontend (Vue.js)
- **Framework**: Vue 3 with Composition API and TypeScript
- **Build Tool**: Vite 5.x with TypeScript support
- **UI Framework**: Ant Design Vue 3
- **State Management**: Pinia 3 (migrated from Vuex)
- **Routing**: Vue Router 4 with hash history
- **Charts**: Uses @antv/g2plot for data visualization
- **Type Checking**: Full TypeScript integration with vue-tsc

### Key API Endpoints
- `/api/kawasaki/patients/` - Patient CRUD operations
- `/api/kawasaki/blood-tests/` - Blood test data
- `/api/kawasaki/liver-functions/` - Liver function tests
- `/api/kawasaki/echocardiography/` - Cardiac imaging data
- `/api/kawasaki/infectious-tests/` - Infectious disease markers
- `/api/kawasaki/samples/` - Sample tracking
- `/api/kawasaki/custom-tests/` - Custom medical tests

## Development Commands

### Frontend Development
```bash
cd frontend

# Install dependencies
npm install

# Development server
npm run dev

# Production build
npm run build

# Lint code
npm run lint

# Type check TypeScript
npm run type-check
```

### Backend Development
```bash
# Install Python dependencies
pip install -r requirements.txt

# Run development server
python manage.py runserver

# Database migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files (for production)
python manage.py collectstatic
```

### Docker Development
```bash
# Build and run with Docker Compose
docker-compose up --build

# Environment variables required in .env:
# DJANGO_SECRET_KEY, DEBUG, DJANGO_LOGLEVEL, DJANGO_ALLOWED_HOSTS
```

## Code Architecture Details

### Django Models Architecture
- **OptimisticLockingModel**: Base abstract model providing optimistic locking via version field
- **Patient**: Central model with foreign key relationships to all test types
- **Medical Test Models**: BloodTest, LiverFunction, Echocardiography, InfectiousTest, CustomTest
- **Sample Management**: Samples model for biological specimen tracking
- **Grouping**: EnrollGroup model for patient categorization

### Vue.js Component Structure
- **Views**: Main page components (LoginView, HomeView, DashboardView, ManagerView)
- **Nested Routes**: Add patient/tests under AddView with dynamic layout
- **Components**: Reusable InlineForm, PatientDetail components
- **Store State**: Token authentication, patient data, groups, test results

### Data Export Features
- All ViewSets include export functionality returning CSV files
- Bulk export available via `/api/kawasaki/export-all/` endpoint
- Uses django-import-export for data serialization

### Authentication Flow
- Token-based authentication using DRF TokenAuthentication
- Frontend stores token in Vuex store
- Router guards prevent unauthenticated access
- Login endpoint: `/api/token-auth/`

## Important Configuration

### Production Settings
- Set `DEBUG = False` in settings.py for production
- Configure `ALLOWED_HOSTS` appropriately
- HTTPS configuration is enabled by default
- Static files served via WhiteNoise middleware

### CORS Configuration
- `CORS_ORIGIN_ALLOW_ALL = True` for development
- Adjust CORS settings for production security

## Development Notes

- The codebase uses Chinese comments and verbose names for medical terms
- All medical data models inherit from OptimisticLockingModel for concurrent access safety
- Frontend uses hash-based routing for better compatibility
- Static files are built into `frontend/dist` and served by Django
- Database uses Asia/Shanghai timezone