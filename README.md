# Task Tracker API

Simple DRF API for personal task management with token auth and owner-only access.

## Setup
- Python 3.11+, virtualenv recommended.
- Install deps: `pip install -r requirements.txt`
- Run migrations: `python manage.py migrate`

## Run
- Start server: `python manage.py runserver`
- Default auth: Token (attach `Authorization: Token <token>` to requests)
- Pagination: Page-number, 10 items per page.

## Endpoints (prefix `/api/`)
- `POST /auth/register/` – create user `{ "username": "...", "password": "..." }`
- `POST /auth/login/` – returns `{ "token": "...", "user_id": 1, "username": "..." }`
- `GET /tasks/` – list your tasks; filters: `?is_done=true|false&priority=1|2|3`
- `POST /tasks/` – create task
- `GET /tasks/<id>/` – retrieve one of your tasks
- `PATCH /tasks/<id>/` – update (partial)
- `DELETE /tasks/<id>/` – delete

## cURL examples
```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"password123"}'

# Login (get token)
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"password123"}'

# Create task
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Authorization: Token <token>" \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy milk","priority":2,"due_date":"2025-12-20"}'

# List with filters
curl -X GET "http://localhost:8000/api/tasks/?is_done=false&priority=3" \
  -H "Authorization: Token <token>"

# Update
curl -X PATCH http://localhost:8000/api/tasks/1/ \
  -H "Authorization: Token <token>" \
  -H "Content-Type: application/json" \
  -d '{"is_done":true}'
```

## Tests
- Run: `python manage.py test`
