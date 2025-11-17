# Recipe Collection REST API

## Overview

A modern RESTful API for managing a recipe collection with user ratings, tags, and search functionality. Built with FastAPI and SQLite, this intermediate project teaches backend development fundamentals including database design, API patterns, authentication, and testing.

Users will be able to:
- Create, read, update, and delete recipes via HTTP endpoints
- Search recipes by ingredients, tags, or cuisine type
- Rate recipes and view average ratings
- Upload recipe images to cloud storage
- Authenticate using JWT tokens for protected routes
- Access comprehensive API documentation via auto-generated Swagger UI

This project bridges the gap between beginner CLI tools and advanced full-stack applications, focusing on backend engineering best practices that apply to production systems.

## Teaching Goals

### Learning Goals
- **RESTful API Design**: Understand resource-based routing, HTTP methods, and status codes
- **Database Modeling**: Design normalized schemas with relationships (one-to-many, many-to-many)
- **SQL & ORMs**: Learn SQLAlchemy for database operations and migrations
- **Authentication & Authorization**: Implement JWT-based auth with user permissions
- **API Testing**: Write comprehensive tests using pytest and httpx
- **Documentation**: Use OpenAPI/Swagger for API documentation

### Technical Goals
- Build a production-ready REST API with proper error handling
- Implement CRUD operations with database persistence
- Design efficient database queries with joins and indexes
- Handle file uploads and cloud storage integration
- Write both unit and integration tests
- Deploy API to a cloud platform (Heroku, Railway, or Fly.io)

### Priority Notes
This project focuses on backend fundamentals that transfer to any language or framework. Understanding REST principles, database design, and testing practices will serve you in every backend project. The FastAPI framework makes modern Python backend development fast and enjoyable while teaching industry-standard patterns.

## Technology Stack

**Backend**: FastAPI
- Reason: Modern, fast, with automatic API documentation
- Built-in data validation using Pydantic
- Async support for high performance
- Best-in-class developer experience

**Storage**: SQLite (development) → PostgreSQL (production)
- Start with SQLite for zero-config local development
- Migrate to PostgreSQL for production deployment
- Same SQLAlchemy code works with both

**ORM**: SQLAlchemy 2.0
- Industry-standard Python ORM
- Type-safe queries with modern 2.0 syntax
- Handles migrations via Alembic

**Key Libraries**:
- `fastapi`: Web framework
- `uvicorn`: ASGI server
- `sqlalchemy`: ORM and database toolkit
- `pydantic`: Data validation and serialization
- `python-jose`: JWT token generation
- `passlib`: Password hashing
- `pytest`: Testing framework
- `httpx`: HTTP client for testing

## Architecture Overview

```
┌──────────────────────────────────────────────┐
│          HTTP Client (Postman, curl, etc.)    │
└─────────────────┬────────────────────────────┘
                  │ HTTP Requests
                  ▼
┌──────────────────────────────────────────────┐
│              FastAPI Application              │
│  ┌────────────────────────────────────────┐  │
│  │  Routers (Endpoints)                   │  │
│  │  - /recipes  (CRUD operations)         │  │
│  │  - /users    (Auth & registration)     │  │
│  │  - /ratings  (Recipe ratings)          │  │
│  └────────────┬───────────────────────────┘  │
│               │                               │
│  ┌────────────▼───────────────────────────┐  │
│  │  Services (Business Logic)             │  │
│  │  - Recipe service                      │  │
│  │  - User service                        │  │
│  │  - Auth service                        │  │
│  └────────────┬───────────────────────────┘  │
│               │                               │
│  ┌────────────▼───────────────────────────┐  │
│  │  SQLAlchemy ORM Layer                  │  │
│  │  - Models (Recipe, User, Rating)       │  │
│  │  - Database session management         │  │
│  └────────────┬───────────────────────────┘  │
└───────────────┼───────────────────────────────┘
                │
                ▼
┌──────────────────────────────────────────────┐
│        SQLite/PostgreSQL Database             │
│  Tables: recipes, users, ratings, tags        │
└──────────────────────────────────────────────┘
```

## Implementation Plan

### Phase 1: Project Setup & Database Foundation (10 steps)

**1. Initialize FastAPI project structure**
- Create directory structure: app/, tests/, migrations/
- Set up virtual environment and requirements.txt
- Initialize git repository
- **What You'll Learn**: Python project organization, dependency management

**2. Configure SQLAlchemy and database connection**
- Create database.py with engine and session factory
- Set up connection string handling for SQLite/PostgreSQL
- Implement get_db() dependency for FastAPI
- **What You'll Learn**: Database connections, dependency injection

**3. Define Recipe model with SQLAlchemy**
- Create models/recipe.py with Recipe table
- Fields: id, title, description, ingredients, instructions, created_at
- Add indexes for common query patterns
- **What You'll Learn**: ORM models, database schema design

**4. Define User model for authentication**
- Create models/user.py with User table
- Fields: id, username, email, hashed_password, created_at
- Add unique constraints on email
- **What You'll Learn**: User management patterns, password security

**5. Define Rating model with foreign keys**
- Create models/rating.py with Rating table
- Fields: id, user_id, recipe_id, score, comment, created_at
- Set up foreign key relationships to User and Recipe
- **What You'll Learn**: Database relationships, foreign keys

**6. Create Tag model and many-to-many relationship**
- Create models/tag.py with Tag table and recipe_tags association table
- Implement many-to-many relationship between Recipe and Tag
- **What You'll Learn**: Advanced relationships, junction tables

**7. Set up Alembic for database migrations**
- Initialize Alembic configuration
- Create initial migration with all models
- Test migration up and down
- **What You'll Learn**: Database migrations, schema version control

**8. Write Pydantic schemas for request/response**
- Create schemas/recipe.py with RecipeCreate, RecipeUpdate, RecipeResponse
- Add validation rules (min length, max length, etc.)
- **What You'll Learn**: Data validation, API contracts

**9. Create database initialization script**
- Script to create tables and seed sample data
- Add 5-10 example recipes for testing
- **What You'll Learn**: Database seeding, initialization patterns

**10. Set up pytest and write first database test**
- Configure pytest with test database
- Write test for creating and querying a recipe
- **What You'll Learn**: Testing setup, test databases

### Phase 2: Core Recipe API Endpoints (10 steps)

**11. Implement GET /recipes (list all recipes)**
- Create routers/recipes.py
- Return paginated list of recipes
- Add query parameters for limit and offset
- **What You'll Learn**: REST routing, pagination

**12. Implement GET /recipes/{id} (get single recipe)**
- Fetch recipe by ID
- Return 404 if not found
- Include relationships (tags, ratings)
- **What You'll Learn**: Path parameters, error responses

**13. Implement POST /recipes (create recipe)**
- Accept RecipeCreate schema in request body
- Validate data and save to database
- Return created recipe with 201 status
- **What You'll Learn**: POST requests, data creation

**14. Implement PUT /recipes/{id} (update recipe)**
- Find recipe by ID
- Update fields from RecipeUpdate schema
- Handle partial updates (only provided fields)
- **What You'll Learn**: PUT vs PATCH, partial updates

**15. Implement DELETE /recipes/{id} (delete recipe)**
- Delete recipe and associated data
- Handle cascading deletes for ratings
- Return 204 No Content on success
- **What You'll Learn**: DELETE operations, cascading

**16. Add search/filter functionality**
- GET /recipes?search=query parameter
- Search in title, description, and ingredients
- Use SQL LIKE or full-text search
- **What You'll Learn**: Database querying, search patterns

**17. Add filtering by tags**
- GET /recipes?tags=italian,vegetarian
- Filter recipes with ANY or ALL specified tags
- Learn query optimization with joins
- **What You'll Learn**: Complex queries, joins

**18. Implement recipe image upload**
- Add image_url field to Recipe model
- Accept file upload in multipart/form-data
- Save to local storage (Phase 4 moves to cloud)
- **What You'll Learn**: File uploads, multipart requests

**19. Write comprehensive tests for recipe endpoints**
- Test all CRUD operations
- Test error cases (not found, validation errors)
- Test pagination and filtering
- **What You'll Learn**: API testing, test coverage

**20. Add API documentation with docstrings**
- Write OpenAPI descriptions for each endpoint
- Add example request/response bodies
- Verify auto-generated Swagger UI at /docs
- **What You'll Learn**: API documentation, OpenAPI spec

### Phase 3: Authentication & Authorization (10 steps)

**21. Implement password hashing utilities**
- Create auth/security.py with hash and verify functions
- Use passlib with bcrypt
- **What You'll Learn**: Password security, hashing

**22. Create user registration endpoint**
- POST /users/register
- Hash password before saving
- Return JWT token on success
- **What You'll Learn**: User registration flow

**23. Create login endpoint**
- POST /users/login with username/password
- Verify credentials and return JWT token
- Return 401 for invalid credentials
- **What You'll Learn**: Authentication flow, JWT basics

**24. Implement JWT token generation**
- Create function to generate access tokens
- Include user_id and expiration in payload
- Sign with secret key from environment variables
- **What You'll Learn**: JWT structure, token signing

**25. Implement JWT token verification**
- Create dependency: get_current_user()
- Decode and verify tokens from Authorization header
- Return user object for valid tokens
- **What You'll Learn**: Token verification, middleware

**26. Protect recipe endpoints with authentication**
- Add get_current_user dependency to POST/PUT/DELETE
- Keep GET endpoints public
- Return 401 for unauthenticated requests
- **What You'll Learn**: Route protection, authorization

**27. Add ownership validation**
- Users can only edit/delete their own recipes
- Add created_by_id foreign key to Recipe model
- Check ownership before allowing modifications
- **What You'll Learn**: Authorization vs authentication

**28. Implement user profile endpoint**
- GET /users/me to get current user info
- Return user data without password hash
- **What You'll Learn**: Authenticated endpoints

**29. Add refresh token functionality (optional)**
- Implement longer-lived refresh tokens
- Create /users/refresh endpoint
- **What You'll Learn**: Refresh token pattern

**30. Write authentication tests**
- Test registration, login, and protected routes
- Test invalid tokens and unauthorized access
- **What You'll Learn**: Security testing

### Phase 4: Ratings, Advanced Features & Polish (10 steps)

**31. Implement POST /recipes/{id}/ratings**
- Allow users to rate recipes (1-5 stars)
- Prevent duplicate ratings from same user
- **What You'll Learn**: Nested resources, constraints

**32. Calculate and display average ratings**
- Add computed field: average_rating to Recipe response
- Use SQL aggregate functions (AVG)
- **What You'll Learn**: Aggregations, computed fields

**33. Implement GET /recipes/{id}/ratings**
- List all ratings for a recipe with pagination
- Include user information in response
- **What You'll Learn**: Nested resource listing

**34. Add recipe favorites/bookmarks**
- Create UserFavorite model (many-to-many)
- Endpoints: POST /recipes/{id}/favorite, DELETE, GET /users/me/favorites
- **What You'll Learn**: User collections, bookmarks

**35. Implement sorting options**
- GET /recipes?sort_by=rating|created_at|title
- Support ascending/descending order
- **What You'll Learn**: Dynamic sorting, query building

**36. Add request rate limiting**
- Use slowapi to limit requests per minute
- Protect against abuse
- **What You'll Learn**: Rate limiting, API protection

**37. Implement comprehensive error handling**
- Custom exception handlers for common errors
- Consistent error response format
- Log errors appropriately
- **What You'll Learn**: Error handling patterns

**38. Add CORS middleware for frontend integration**
- Configure CORS to allow requests from frontend domains
- Set appropriate headers
- **What You'll Learn**: CORS, cross-origin requests

**39. Optimize database queries**
- Add eager loading for relationships (joinedload)
- Create database indexes for common queries
- Profile slow queries
- **What You'll Learn**: Query optimization, performance

**40. Add API versioning**
- Implement /v1/ prefix for all routes
- Set up structure for future v2
- **What You'll Learn**: API versioning strategies

### Phase 5: Deployment & Production Readiness (10 steps)

**41. Set up environment variable management**
- Create .env.example file
- Use python-dotenv for local development
- Document all required variables
- **What You'll Learn**: Configuration management, secrets

**42. Create Docker configuration**
- Write Dockerfile for containerized deployment
- Create docker-compose.yml for local development
- **What You'll Learn**: Docker, containerization

**43. Migrate from SQLite to PostgreSQL**
- Update connection string
- Test migrations on PostgreSQL
- **What You'll Learn**: Database migration, PostgreSQL

**44. Set up cloud file storage (S3 or equivalent)**
- Replace local file storage with cloud bucket
- Use boto3 or similar library
- **What You'll Learn**: Cloud storage, S3 APIs

**45. Add logging and monitoring**
- Configure structured logging
- Add request ID tracking
- Set up error tracking (Sentry optional)
- **What You'll Learn**: Production logging, observability

**46. Write API integration tests**
- End-to-end tests for complete workflows
- Test authentication + CRUD in sequence
- **What You'll Learn**: Integration testing

**47. Deploy to cloud platform**
- Deploy to Railway, Fly.io, or Heroku
- Configure production database
- Set environment variables
- **What You'll Learn**: Cloud deployment, production environments

**48. Set up CI/CD pipeline**
- Create GitHub Actions workflow
- Run tests on every push
- Auto-deploy on successful tests
- **What You'll Learn**: CI/CD, automation

**49. Write comprehensive API documentation**
- Create README with setup and usage instructions
- Document all endpoints with curl examples
- Add architecture diagrams
- **What You'll Learn**: Technical documentation

**50. Load testing and final optimization**
- Use tools like Locust or wrk for load testing
- Identify and fix performance bottlenecks
- Verify API handles expected load
- **What You'll Learn**: Performance testing, scalability

## Global Teaching Notes

### Why This Project?
Recipe APIs are excellent learning projects because:
- **Relatable domain**: Everyone understands recipes, so you focus on technical learning
- **Rich data model**: Multiple entities with various relationship types
- **Real-world patterns**: Authentication, search, ratings are universal features
- **Practical skills**: RESTful APIs are the backbone of modern web applications

### Key Concepts You'll Master
1. **REST Principles**: Resources, HTTP methods, status codes, and idempotency
2. **Database Design**: Normalization, relationships, indexes, and migrations
3. **Authentication**: Stateless auth with JWTs, password security, protected routes
4. **Testing**: Unit tests, integration tests, test databases, and mocking

### Common Pitfalls
- **N+1 query problem**: Use eager loading (joinedload) to avoid multiple queries
- **Password security**: Never store plain passwords; always hash with bcrypt
- **SQL injection**: SQLAlchemy protects you, but be careful with raw SQL
- **Token security**: Keep secret keys in environment variables, not code

### Extension Ideas
- **Recipe recommendations**: Use collaborative filtering based on ratings
- **Meal planning**: Create endpoints for weekly meal plans
- **Nutrition data**: Integrate with nutrition APIs for calorie/macro tracking
- **Social features**: Follow other users, share recipes, comments
- **Admin panel**: Build Streamlit dashboard for content moderation

## Setup Instructions

### Prerequisites
- Python 3.9+
- PostgreSQL (for production) or SQLite (for development)
- Git

### Local Development

1. **Clone repository**
   ```bash
   git clone <repo-url>
   cd recipe-api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start development server**
   ```bash
   uvicorn app.main:app --reload
   ```

7. **Access API documentation**
   - OpenAPI docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Running Tests
```bash
pytest tests/ -v --cov=app
```

### Docker Deployment
```bash
docker-compose up --build
```

## Success Metrics

✅ All CRUD endpoints working with proper status codes
✅ Authentication required for protected routes
✅ Database relationships correctly implemented
✅ Test coverage above 80%
✅ API deployed and accessible publicly
✅ OpenAPI documentation complete and accurate
✅ Response times under 200ms for typical queries
✅ Can handle 100+ concurrent requests

## Next Steps

1. **Build a frontend**: Create React or Vue app consuming this API
2. **Add GraphQL**: Implement GraphQL layer alongside REST
3. **Microservices**: Split into separate services (recipes, users, ratings)
4. **Event-driven**: Add message queue for notifications and background tasks
5. **Advanced search**: Implement Elasticsearch for better recipe search

This project gives you production-ready backend skills applicable to any API you'll build in your career.
