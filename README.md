# AI Interview Preparation Platform

A comprehensive AI-powered interview coaching platform that helps candidates prepare for technical and behavioral interviews with personalized feedback, mock interviews, and skill assessments.

## 🎯 Features

- **Resume Upload & ATS Scoring** - Analyze resumes with AI-powered ATS scoring
- **Mock Interviews** - AI-generated technical and behavioral interview questions
- **Coding Question Recommendations** - Personalized coding challenges by difficulty
- **Speech/Text Feedback** - Real-time feedback on interview responses
- **Analytics Dashboard** - Track progress and improvement over time
- **Personalized Learning Roadmap** - Adaptive learning paths based on performance

## 🏗️ Tech Stack

### Backend
- **Python 3.11** with FastAPI
- **PostgreSQL** - Primary database
- **Redis** - Caching and session management
- **SQLAlchemy** - ORM for database operations
- **Pydantic** - Data validation
- **JWT** - Secure authentication

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first styling
- **Zustand** - Lightweight state management
- **Axios** - HTTP client
- **React Hot Toast** - Notifications

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **PostgreSQL 15** - Database
- **Redis 7** - In-memory cache

## 📁 Project Structure

```
ai-interview-platform/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── config.py            # Configuration settings
│   │   ├── database.py          # Database setup
│   │   ├── models/              # SQLAlchemy models
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── routes/              # API endpoints
│   │   ├── services/            # Business logic
│   │   └── utils/               # Utility functions
│   ├── tests/                   # Test suite
│   ├── requirements.txt         # Python dependencies
│   ├── Dockerfile              # Backend container
│   └── .env.example            # Environment template
├── frontend/
│   ├── src/
│   │   ├── app/                # Next.js pages
│   │   ├── components/         # React components
│   │   ├── lib/                # Utilities (API, store)
│   │   └── styles/             # Global styles
│   ├── package.json            # Node dependencies
│   ├── Dockerfile             # Frontend container
│   └── .env.local.example     # Environment template
├── docker-compose.yml         # Container orchestration
└── README.md                  # This file
```

## 🚀 Quick Start (Recommended)

### Prerequisites
- Docker & Docker Compose installed
- Git installed

### Installation Steps

1. **Clone the repository**
```bash
git clone https://github.com/chakradharrakhonde/ai-interview-platform.git
cd ai-interview-platform
```

2. **Create environment files**
```bash
cp backend/.env.example backend/.env
cp frontend/.env.local.example frontend/.env.local
```

3. **Update backend environment (optional)**
```bash
# Edit backend/.env
DATABASE_URL=postgresql://interview_user:interview_password@postgres:5432/interview_db
REDIS_URL=redis://redis:6379
SECRET_KEY=your-super-secret-key-here
OPENAI_API_KEY=sk-your-openai-key-here  # Optional for demo
ENVIRONMENT=development
DEBUG=True
```

4. **Start all services**
```bash
docker-compose up -d
```

5. **Verify services are running**
```bash
# Check container status
docker-compose ps

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## 🛠️ Local Development (Without Docker)

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run the application
uvicorn app.main:app --reload
# Server runs on http://localhost:8000
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.local.example .env.local

# Run development server
npm run dev
# Application runs on http://localhost:3000
```

## 📚 API Documentation

Once the backend is running, visit:
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

#### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh token
- `POST /api/v1/auth/logout` - User logout

#### Resume Management
- `POST /api/v1/resumes/upload` - Upload resume
- `GET /api/v1/resumes/{resume_id}` - Get resume details
- `POST /api/v1/resumes/{resume_id}/score` - Get ATS score
- `DELETE /api/v1/resumes/{resume_id}` - Delete resume

#### Mock Interviews
- `POST /api/v1/interviews/start` - Start interview
- `POST /api/v1/interviews/{interview_id}/answer` - Submit answer
- `GET /api/v1/interviews/{interview_id}/feedback` - Get feedback
- `GET /api/v1/interviews/history` - Get interview history

#### Coding Questions
- `GET /api/v1/coding/questions` - Get questions by difficulty
- `GET /api/v1/coding/questions/{question_id}` - Get question details
- `POST /api/v1/coding/submit` - Submit code solution

#### Dashboard
- `GET /api/v1/dashboard/stats` - Get user statistics
- `GET /api/v1/health` - Health check endpoint

## 🔐 Security Features

- JWT authentication with access/refresh tokens
- Password hashing with bcrypt
- CORS configuration
- SQL injection prevention via ORM
- Secure file upload handling
- Environment-based configuration
- Rate limiting ready

## 📊 Database Models

### Users
- Email (unique, indexed)
- Password hash
- First/Last name
- Verification status
- Timestamps

### Resumes
- File path and name
- ATS score
- Parsed data (JSON)
- Skills array
- Experience years

### Interviews
- Type (behavioral/technical/coding)
- Status (started/in_progress/completed)
- Score and feedback
- Duration tracking

### Coding Questions
- Title and description
- Difficulty level
- Test cases
- Time/memory limits

## 🧪 Testing

### Run Backend Tests
```bash
cd backend
pytest                    # Run all tests
pytest -v               # Verbose output
pytest --cov           # With coverage report
```

### Run Frontend Tests
```bash
cd frontend
npm test                # Run all tests
npm test -- --watch   # Watch mode
```

## 🚢 Deployment

### Docker Deployment

```bash
# Build production images
docker-compose -f docker-compose.yml build

# Run in production mode
DEBUG=False ENVIRONMENT=production docker-compose up -d
```

### Environment Variables for Production

Update these in production:
- `SECRET_KEY` - Strong random key
- `DEBUG` - Set to `False`
- `ENVIRONMENT` - Set to `production`
- `DATABASE_URL` - Production database URL
- `OPENAI_API_KEY` - Your OpenAI API key

## 📖 Frontend Pages

- `/` - Landing page
- `/auth/login` - Login page
- `/auth/register` - Registration page
- `/dashboard` - User dashboard with statistics
- `/resume` - Resume upload and ATS scoring
- `/interview` - Mock interview practice
- `/coding` - Coding practice with problems

## 🎨 UI Components

Reusable components in `frontend/src/components/`:
- `Button` - Customizable button with variants
- `Input` - Form input with validation
- `Card` - Container component
- `Navbar` - Navigation bar
- `LoginForm` - Authentication form
- `RegisterForm` - Registration form
- `ResumeUploader` - Resume upload interface
- `MockInterview` - Interview practice interface

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Change port in docker-compose.yml or use different ports
docker-compose up -d --scale frontend=0
```

### Database Connection Error
```bash
# Check if PostgreSQL is running
docker-compose logs postgres

# Rebuild database
docker-compose down -v
docker-compose up -d
```

### API Not Responding
```bash
# Check backend logs
docker-compose logs backend

# Ensure backend is healthy
docker-compose ps
```

## 📝 Development Workflow

1. Create a feature branch
   ```bash
   git checkout -b feature/your-feature
   ```

2. Make changes and test
   ```bash
   # Backend changes auto-reload with --reload flag
   # Frontend changes auto-reload with npm run dev
   ```

3. Commit changes
   ```bash
   git add .
   git commit -m "Add your feature"
   ```

4. Push to GitHub
   ```bash
   git push origin feature/your-feature
   ```

5. Create a Pull Request

## 📦 Dependencies

### Backend
- fastapi - Web framework
- sqlalchemy - ORM
- pydantic - Data validation
- psycopg2 - PostgreSQL adapter
- redis - Caching
- python-jose - JWT handling
- passlib - Password hashing

### Frontend
- react - UI library
- next - React framework
- zustand - State management
- axios - HTTP client
- tailwindcss - Styling
- react-hot-toast - Notifications

## 📞 Support & Contribution

- For issues: Open a GitHub issue
- For contributions: Submit a pull request
- For questions: Check the docs folder

## 📄 License

MIT License - see LICENSE file for details

## 👨‍💻 Author

Chakradhar Rakhonde - [@chakradharrakhonde](https://github.com/chakradharrakhonde)

---

**Happy Interview Preparation! 🎉**
