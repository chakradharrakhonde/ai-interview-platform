# AI Interview Preparation Platform

A comprehensive AI-powered interview coaching platform that helps candidates prepare for technical and behavioral interviews with personalized feedback, mock interviews, and skill assessments.

## 🎯 Features

- **Resume Upload & ATS Scoring** - Analyze resumes with AI-powered ATS scoring
- **Mock Interviews** - AI-generated technical and behavioral interview questions
- **Coding Question Recommendations** - Personalized coding challenges based on role
- **Speech/Text Feedback** - Real-time feedback on interview responses
- **Personalized Learning Roadmap** - Adaptive learning paths based on performance
- **Analytics Dashboard** - Track progress and improvement over time

## 🏗️ Tech Stack

### Backend
- **Python 3.10+** with FastAPI
- **PostgreSQL** - Primary database
- **Redis** - Caching and session management
- **OpenAI API** - LLM integration for question generation and feedback
- **Pydantic** - Data validation

### Frontend
- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **ShadcN/UI** - Component library
- **Zustand** - State management

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **PostgreSQL** - Database
- **Redis** - In-memory cache

## 📁 Project Structure

```
ai-interview-platform/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models/         # Pydantic models
│   │   ├── schemas/        # Database schemas
│   │   ├── routes/         # API endpoints
│   │   ├── services/       # Business logic
│   │   ├── utils/          # Utilities
│   │   └── middleware/     # Custom middleware
│   ├── alembic/            # Database migrations
│   ├── tests/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # App directory
│   │   ├── components/    # React components
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── lib/
│   │   ├── styles/
│   │   └── types/
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── Dockerfile
│   └── .env.local.example
├── docker-compose.yml
├── .github/
│   └── workflows/         # CI/CD workflows
├── docs/                  # Documentation
└── .gitignore
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Redis 7+

### Development Setup

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

3. **Update environment variables**
   ```bash
   # backend/.env
   OPENAI_API_KEY=your_key_here
   DATABASE_URL=postgresql://user:password@localhost:5432/interview_db
   REDIS_URL=redis://localhost:6379
   SECRET_KEY=your_secret_key_here
   ```

4. **Start services with Docker Compose**
   ```bash
   docker-compose up -d
   ```

5. **Run database migrations**
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

6. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 📚 API Documentation

### Authentication
- POST `/api/v1/auth/register` - Register new user
- POST `/api/v1/auth/login` - User login
- POST `/api/v1/auth/refresh` - Refresh token
- POST `/api/v1/auth/logout` - User logout

### Resume Management
- POST `/api/v1/resumes/upload` - Upload resume
- GET `/api/v1/resumes/{resume_id}` - Get resume
- DELETE `/api/v1/resumes/{resume_id}` - Delete resume
- POST `/api/v1/resumes/{resume_id}/score` - Get ATS score

### Mock Interviews
- POST `/api/v1/interviews/start` - Start mock interview
- POST `/api/v1/interviews/{interview_id}/answer` - Submit answer
- GET `/api/v1/interviews/{interview_id}/feedback` - Get feedback
- GET `/api/v1/interviews/history` - Interview history

### Coding Questions
- GET `/api/v1/coding/questions` - Get recommended questions
- GET `/api/v1/coding/questions/{question_id}` - Get question details
- POST `/api/v1/coding/submit` - Submit solution

### Learning Roadmap
- GET `/api/v1/roadmap` - Get personalized roadmap
- PUT `/api/v1/roadmap/update` - Update roadmap progress

## 🗄️ Database Schema

### Users
- id, email, password_hash, first_name, last_name, created_at, updated_at

### Resumes
- id, user_id, file_path, ats_score, parsed_data, created_at

### Interviews
- id, user_id, type, status, feedback, started_at, completed_at

### Interview Answers
- id, interview_id, question_id, text_response, audio_url, feedback

### Coding Questions
- id, difficulty, topic, title, description, test_cases

### Learning Roadmap
- id, user_id, topics, progress, recommendations

## 🔐 Security Features

- JWT authentication with access/refresh tokens
- Password hashing with bcrypt
- CORS configuration
- Rate limiting
- SQL injection prevention via ORM
- Secure file upload handling
- Environment-based configuration

## 🧪 Testing

```bash
# Run backend tests
docker-compose exec backend pytest

# Run frontend tests
docker-compose exec frontend npm test
```

## 📊 Performance & Caching

- Redis caching for frequently accessed data
- Database connection pooling
- Async operations for long-running tasks
- Pagination for large datasets

## 🚢 Deployment

### Production Checklist
- [ ] Environment variables configured
- [ ] Database backups configured
- [ ] SSL/TLS certificates setup
- [ ] Rate limiting configured
- [ ] Monitoring/logging setup
- [ ] CI/CD pipelines active

### Deployment Guides
- [Docker Deployment](./docs/deployment/docker.md)
- [AWS Deployment](./docs/deployment/aws.md)
- [Heroku Deployment](./docs/deployment/heroku.md)

## 📝 API Response Format

All endpoints follow this format:

```json
{
  "success": true,
  "data": {},
  "message": "Success message",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Run tests and linting
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 👨‍💻 Author

Chakradhar Rakhonde - [@chakradharrakhonde](https://github.com/chakradharrakhonde)

## 📞 Support

For issues and questions, please open an GitHub issue.

---

**Happy Interview Preparation! 🎉**
