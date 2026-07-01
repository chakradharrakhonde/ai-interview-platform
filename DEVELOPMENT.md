# Development Guide

## Project Architecture

### Backend Architecture

```
FastAPI Application
├── Routes (HTTP endpoints)
├── Services (Business logic)
├── Models (Database schemas)
├── Schemas (Request/Response validation)
└── Database (PostgreSQL with SQLAlchemy)
```

### Frontend Architecture

```
Next.js Application
├── Pages (Route components)
├── Components (Reusable UI)
├── Lib (API client, state management)
└── Styles (Tailwind CSS)
```

## Adding a New Feature

### 1. Backend Feature

1. Create model in `backend/app/models/`
2. Create schema in `backend/app/schemas/`
3. Create service logic in `backend/app/services/`
4. Create routes in `backend/app/routes/`
5. Add tests in `backend/tests/`

### 2. Frontend Feature

1. Create component in `frontend/src/components/`
2. Create page in `frontend/src/app/` (if needed)
3. Add API calls in `frontend/src/lib/api.ts`
4. Add store actions if needed in `frontend/src/lib/store.ts`

## API Development

### Creating an Endpoint

```python
# backend/app/routes/example.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()

@router.get("/example")
async def get_example(db: Session = Depends(get_db)):
    """Example endpoint"""
    return {"message": "success"}
```

### Frontend API Call

```typescript
// frontend/src/lib/api.ts
export const exampleAPI = {
  getExample: () => api.get('/api/v1/example'),
};

// frontend/src/components/Example.tsx
const handleFetch = async () => {
  const response = await exampleAPI.getExample();
  console.log(response.data);
};
```

## Database Operations

### Creating a New Model

```python
# backend/app/models/example.py
from sqlalchemy import Column, String, DateTime
from datetime import datetime
from app.database import Base

class Example(Base):
    __tablename__ = "examples"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
```

### Creating a Schema

```python
# backend/app/schemas/example.py
from pydantic import BaseModel
from typing import Optional

class ExampleCreate(BaseModel):
    name: str

class ExampleResponse(BaseModel):
    id: str
    name: str
    
    class Config:
        from_attributes = True
```

## State Management

### Using Zustand Store

```typescript
// frontend/src/lib/store.ts
interface ExampleStore {
  data: any;
  setData: (data: any) => void;
}

export const useExampleStore = create<ExampleStore>((set) => ({
  data: null,
  setData: (data) => set({ data }),
}));

// In component
const MyComponent = () => {
  const { data, setData } = useExampleStore();
  // Use data and setData
};
```

## Testing

### Backend Test Example

```python
# backend/tests/test_example.py
def test_get_example(client):
    response = client.get("/api/v1/example")
    assert response.status_code == 200
    assert response.json()["message"] == "success"
```

### Frontend Test Example

```typescript
// frontend/src/components/__tests__/Example.test.tsx
import { render, screen } from '@testing-library/react';
import Example from '../Example';

test('renders example', () => {
  render(<Example />);
  expect(screen.getByText(/example/i)).toBeInTheDocument();
});
```

## Code Style

### Backend
- Follow PEP 8
- Use type hints
- Write docstrings
- Use meaningful variable names

### Frontend
- Use TypeScript
- Write JSDoc comments
- Use functional components
- Keep components small and reusable

## Git Workflow

1. Create feature branch: `git checkout -b feature/name`
2. Make changes and commit: `git commit -m "description"`
3. Push to GitHub: `git push origin feature/name`
4. Create Pull Request
5. Wait for review and merge

## Performance Tips

### Backend
- Use database indexes for frequent queries
- Cache frequently accessed data in Redis
- Use async operations for I/O
- Implement pagination for large datasets

### Frontend
- Use React.memo for expensive components
- Implement code splitting with dynamic imports
- Optimize images
- Use Zustand selectors to avoid unnecessary re-renders

## Security Considerations

- Always validate user input
- Use JWT tokens for authentication
- Hash passwords with bcrypt
- Sanitize file uploads
- Use environment variables for secrets
- Implement rate limiting
- Use CORS properly

## Debugging

### Backend Debugging
```python
import pdb; pdb.set_trace()  # Breakpoint
print(data)  # Console output
```

### Frontend Debugging
```typescript
console.log(data);  // Console output
debugger;  // Browser debugpoint
```

For more detailed debugging, use:
- Backend: VS Code Python debugger
- Frontend: Chrome DevTools

## Common Issues & Solutions

### CORS Issues
Ensure `CORS_ORIGINS` is properly configured in backend

### Authentication Fails
Check JWT token expiration and SECRET_KEY

### Database Errors
Ensure PostgreSQL is running and connection string is correct

### File Upload Issues
Check file size limits and upload directory permissions

## Additional Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Next.js Docs](https://nextjs.org/docs)
- [React Docs](https://react.dev)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
