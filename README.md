# recipie-API-APP
# Recipe API

A production-grade REST API built with Django REST Framework, PostgreSQL, and Docker. The project covers custom authentication, relational data modelling, serializer design, and a full DevOps setup with CI/CD — built as a learning project to understand how the full Django/DRF stack fits together end to end.

---

## Features

- Custom email-based authentication with token auth on all protected endpoints
- Full CRUD for recipes, tags, and ingredients with user-scoped data isolation
- Relational model — recipes link to tags and ingredients via ManyToMany
- TDD throughout — 90%+ test coverage using Django's APIClient
- Containerised with Docker and Docker Compose for consistent environments
- Automated linting (flake8) and test runs via GitHub Actions CI/CD

---

## Tech Stack

- Python 3 / Django / Django REST Framework
- PostgreSQL
- Docker / Docker Compose
- GitHub Actions
- flake8

---

## Project Structure

```
app/
├── core/          # Custom user model, database models
├── user/          # Registration, token auth endpoints
└── recipe/        # Recipe, tag, ingredient endpoints, serializers, tests
```

---

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/user/create/` | POST | Register a new user |
| `/api/user/token/` | POST | Obtain auth token |
| `/api/user/me/` | GET / PATCH | View and update profile |
| `/api/recipe/recipes/` | GET / POST | List and create recipes |
| `/api/recipe/recipes/{id}/` | GET / PUT / PATCH / DELETE | Manage a specific recipe |
| `/api/recipe/tags/` | GET / POST | List and create tags |
| `/api/recipe/ingredients/` | GET / POST | List and create ingredients |

All recipe, tag, and ingredient endpoints require authentication. Each user can only access their own data.

---

## Authentication

Token-based authentication throughout. Users register at `/api/user/create/`, then POST credentials to `/api/user/token/` to receive a token. All subsequent requests include the token in the Authorization header:

```
Authorization: Token <your_token>
```

---

## Key Design Decisions

**Custom user model** — replaced Django's default username-based User with a custom model using email as the primary identifier. The custom `UserManager` overrides `create_user()` to call `set_password()` before saving, ensuring passwords are always hashed.

**Serializer design** — `UserSerializer` implements a custom `create()` that routes through `create_user()` rather than a direct `Model.objects.create()`. The `update()` method pops the password from `validated_data` before passing the rest to `super().update()`, then calls `set_password()` separately so re-hashing is always applied correctly.

**Data isolation** — `RecipeViewSet` overrides `get_queryset()` to filter `Recipe.objects.all()` down to only the authenticated user's recipes. Users cannot access each other's data at any endpoint.

**TDD** — tests were written before implementation throughout. `APIClient` simulates both authenticated and unauthenticated HTTP requests. Tests cover registration, token issuance, permission enforcement, and full CRUD operations on recipes, tags, and ingredients.

---

## Running Locally

```bash
# Clone the repo
git clone https://github.com/niniolaman1/recipie-API-APP.git
cd recipie-API-APP

# Start the containers
docker-compose up

# Run tests
docker-compose run --rm app sh -c "python manage.py test"

# Run linting
docker-compose run --rm app sh -c "flake8"
```

---

## CI/CD

GitHub Actions runs on every push to main — linting with flake8 and the full test suite. The workflow is defined in `.github/workflows/`.
