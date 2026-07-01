# Setup Instructions

## Prerequisites

- Docker & Docker Compose
- Git
- (Optional) Python 3.11+ for local development
- (Optional) Node.js 18+ for local frontend development

## Quick Start with Docker (Recommended)

### 1. Clone Repository
```bash
git clone https://github.com/chakradharrakhonde/ai-interview-platform.git
cd ai-interview-platform
```

### 2. Configure Environment
```bash
cp backend/.env.example backend/.env
cp frontend/.env.local.example frontend/.env.local
```

### 3. Start Services
```bash
docker-compose up -d
```

### 4. Access Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 5. Create Test User
1. Go to http://localhost:3000
2. Click "Register"
3. Fill in registration details
4. Login with your credentials

## Local Development Setup

### Backend (Python)

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database (requires PostgreSQL running)
cp .env.example .env
# Edit .env and update DATABASE_URL

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

### Frontend (Node.js)

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.local.example .env.local

# Start development server
npm run dev
```

## Docker Commands

```bash
# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop services
docker-compose down

# Rebuild containers
docker-compose build

# Remove volumes (reset database)
docker-compose down -v

# Run commands in container
docker-compose exec backend python -m pytest
```

## Troubleshooting

### Ports in Use
If ports 3000, 8000, 5432, or 6379 are already in use:
1. Stop existing services
2. Or change ports in docker-compose.yml

### Database Connection Issues
```bash
# Reset database
docker-compose down -v
docker-compose up -d postgres
# Wait for postgres to start, then start other services
docker-compose up -d
```

### Hot Reload Not Working
Ensure volume mounts are correct in docker-compose.yml

## Environment Variables

Key variables to configure:

**Backend (.env)**
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `SECRET_KEY` - JWT secret key
- `OPENAI_API_KEY` - OpenAI API key (optional for demo)
- `DEBUG` - Set to False in production

**Frontend (.env.local)**
- `NEXT_PUBLIC_API_URL` - Backend API URL

## Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Building for Production

```bash
# Build production images
docker-compose build

# Run with production settings
DEBUG=False ENVIRONMENT=production docker-compose up -d
```

## Next Steps

1. Explore the API at http://localhost:8000/docs
2. Try uploading a resume
3. Practice mock interviews
4. Solve coding problems
5. Check your dashboard statistics

For more information, see README.md
