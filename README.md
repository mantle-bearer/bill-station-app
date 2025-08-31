# Bill Station Auth Service

A Django-based user authentication system with JWT tokens, Redis caching for password reset, and PostgreSQL database integration.

## Features

- ✅ User Registration with email as username
- ✅ JWT-based Authentication
- ✅ Password Reset with Redis-cached tokens
- ✅ PostgreSQL Database Integration
- ✅ API Documentation with Swagger/OpenAPI
- ✅ Docker Support
- ✅ Unit Tests
- ✅ Production-ready Deployment Configuration

## Tech Stack

- **Backend**: Django 4.2 + Django REST Framework
- **Database**: PostgreSQL
- **Cache**: Redis
- **Authentication**: JWT (Simple JWT)
- **Documentation**: drf-yasg (Swagger/OpenAPI)
- **Deployment**: Railway/Render ready with Gunicorn + WhiteNoise

## Quick Start

### 1. Local Development with Docker

```bash
# Clone the repository
git clone <your-repo-url>
cd auth_service

# Build and run with Docker Compose
docker-compose up --build

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser (optional)
docker-compose exec web python manage.py createsuperuser

# Access the application
# API: http://localhost:8000
# Swagger: http://localhost:8000/swagger/
# Admin: http://localhost:8000/admin/
```

### 2. Manual Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database and Redis credentials

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

## Environment Variables

Create a `.env` file in the project root:

```bash
# Database Configuration
DB_NAME=your_postgres_db_name
DB_USER=your_postgres_username
DB_PASSWORD=your_postgres_password
DB_HOST=your_postgres_host
DB_PORT=5432

# Alternative: Use DATABASE_URL for deployment platforms
# DATABASE_URL=postgresql://user:password@host:port/database

# Redis Configuration
REDIS_URL=redis://your_redis_host:6379/1

# Django Configuration
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
```

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register/` | User registration | No |
| POST | `/api/auth/login/` | User login | No |
| POST | `/api/auth/forgot-password/` | Request password reset | No |
| POST | `/api/auth/reset-password/` | Reset password with token | No |
| GET | `/api/auth/profile/` | Get user profile | Yes |
| GET | `/swagger/` | API Documentation | No |

### Example Usage

#### 1. Register a new user
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "full_name": "John Doe",
    "password": "StrongPassword123!",
    "password_confirm": "StrongPassword123!"
  }'
```

#### 2. Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "StrongPassword123!"
  }'
```

#### 3. Access protected endpoint
```bash
curl -X GET http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### 4. Forgot Password
```bash
curl -X POST http://localhost:8000/api/auth/forgot-password/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com"
  }'
```

#### 5. Reset Password
```bash
curl -X POST http://localhost:8000/api/auth/reset-password/ \
  -H "Content-Type: application/json" \
  -d '{
    "token": "RESET_TOKEN_FROM_STEP_4",
    "new_password": "NewStrongPassword123!",
    "confirm_password": "NewStrongPassword123!"
  }'
```

## Deployment

### Railway Deployment

1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard:
   - `DATABASE_URL` (Railway PostgreSQL)
   - `REDIS_URL` (Railway Redis)
   - `SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS=*.up.railway.app,your-domain.com`

3. Deploy automatically on push to main branch

### Render Deployment

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set environment variables:
   - `DATABASE_URL` (Render PostgreSQL)
   - `REDIS_URL` (Render Redis)
   - `SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS=*.onrender.com,your-domain.com`

4. Set build command: `pip install -r requirements.txt`
5. Set start command: `gunicorn auth_service.wsgi:application`

## Testing

```bash
# Run all tests
python manage.py test

# Run specific test
python manage.py test accounts.tests.UserRegistrationTestCase

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## Security Features

- ✅ JWT tokens with access/refresh token rotation
- ✅ Password validation with Django validators
- ✅ Secure password reset with Redis-cached tokens (10-minute expiry)
- ✅ CORS protection
- ✅ Environment-based configuration
- ✅ Rate limiting ready (implement with django-ratelimit if needed)

## Development Notes

- The password reset token is returned in the API response for testing purposes
- In production, send the reset token via email instead
- Redis is used for caching reset tokens with automatic expiry
- All passwords are hashed using Django's built-in password hashers
- JWT tokens include both access and refresh tokens for secure authentication

## Live Demo

🚀 **Deployed Application**: [Your Railway/Render URL here]

📚 **API Documentation**: [Your Railway/Render URL]/swagger/

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request
```
```