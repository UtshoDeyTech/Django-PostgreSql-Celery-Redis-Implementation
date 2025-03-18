# Django REST Framework with Celery, Redis, and PostgreSQL

This guide explains the Django project with two apps - a User app for CRUD operations and a Celery Worker app to track task status. The application uses Celery for asynchronous task processing, Redis as a message broker, and PostgreSQL for data storage.

## Project Structure

```
django_task_project/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── init.ps1
├── manage.py
├── .env
├── task_project/        # Django project
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── celery_worker_app/   # Celery worker app for task tracking
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   │   └── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
└── user_app/            # User app for CRUD operations
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── migrations/
    │   └── __init__.py
    ├── models.py
    ├── serializers.py
    ├── tasks.py
    ├── urls.py
    └── views.py
```

## How The System Works

1. When a client sends a request to a User API endpoint:
   - The request is handled by Django
   - Django creates a Task record in the database through the celery_worker_app
   - Django dispatches an asynchronous task to Celery via Redis
   - The client receives a task ID that can be used to check the status

2. The Celery worker:
   - Picks up the task from Redis
   - Processes it (in this case, performs CRUD operations on User model)
   - Updates the task's status and progress in the database

3. The client can check the status of the task by making requests to the Task API endpoints.

## Getting Started

### Prerequisites

- Docker and Docker Compose

### Setup

1. Create a `.env` file using the provided template
2. Start the services using Docker Compose:

```bash
docker-compose up -d
```

This will start four services:
- Django web server on port 8000
- PostgreSQL database on port 5432
- Redis on port 6379
- Celery worker

## API Endpoints

### User API

The User API provides the following endpoints:

1. **List all users**
   - `GET /api/users/`
   - Creates a task to list all users
   - Returns a task ID for checking the status

2. **Get a single user**
   - `GET /api/users/{user_id}/`
   - Creates a task to get a specific user
   - Returns a task ID for checking the status

3. **Create a new user**
   - `POST /api/users/`
   - Request body: `{"username": "user1", "email": "user1@example.com", "first_name": "John", "last_name": "Doe"}`
   - Creates a task to create a new user
   - Returns a task ID for checking the status

4. **Update a user**
   - `PUT /api/users/{user_id}/` or `PATCH /api/users/{user_id}/`
   - Request body with fields to update: `{"email": "newemail@example.com"}`
   - Creates a task to update a user
   - Returns a task ID for checking the status

5. **Delete a user**
   - `DELETE /api/users/{user_id}/`
   - Creates a task to delete a user
   - Returns a task ID for checking the status

### Task API

The Task API provides the following endpoints:

1. **List all tasks**
   - `GET /api/tasks/`
   - Returns a list of all tasks with basic information

2. **Get task details**
   - `GET /api/tasks/{task_id}/`
   - Returns detailed information about a specific task

3. **Get task status**
   - `GET /api/tasks/{task_id}/status/`
   - Returns the current status of a task, including progress and results if completed

## Example Usage

### 1. Create a New User

```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user1", "email": "user1@example.com", "first_name": "John", "last_name": "Doe"}'
```

Response:
```json
{
  "task_id": "12345-abcde",
  "message": "Task created to create user user1",
  "status_endpoint": "/api/tasks/12345-abcde/status/"
}
```

### 2. Check Task Status

```bash
curl http://localhost:8000/api/tasks/12345-abcde/status/
```

Response (while processing):
```json
{
  "id": "12345-abcde",
  "status": "PROCESSING",
  "task_name": "create_user",
  "created_at": "2025-03-18T10:15:30Z",
  "updated_at": "2025-03-18T10:15:35Z",
  "input_data": {
    "username": "user1",
    "email": "user1@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "result": {"progress": 40},
  "progress": 40,
  "related_table": "user",
  "related_id": null,
  "operation": "CREATE"
}
```

Response (when completed):
```json
{
  "id": "12345-abcde",
  "status": "DONE",
  "task_name": "create_user",
  "created_at": "2025-03-18T10:15:30Z",
  "updated_at": "2025-03-18T10:15:50Z",
  "input_data": {
    "username": "user1",
    "email": "user1@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "result": {
    "success": true,
    "user_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "message": "Successfully created user user1",
    "progress": 100
  },
  "progress": 100,
  "related_table": "user",
  "related_id": null,
  "operation": "CREATE"
}
```

### 3. Update a User

```bash
curl -X PATCH http://localhost:8000/api/users/f47ac10b-58cc-4372-a567-0e02b2c3d479/ \
  -H "Content-Type: application/json" \
  -d '{"email": "newemail@example.com"}'
```

Response:
```json
{
  "task_id": "67890-fghij",
  "message": "Task created to update user f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "status_endpoint": "/api/tasks/67890-fghij/status/"
}
```

## Administration

You can access the Django admin interface at `http://localhost:8000/admin/` to manage users and tasks directly.

If you want to create a superuser, uncomment and set the appropriate values in the `.env` file:

```
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=adminpassword
```

Then restart the containers.

## Technical Details

### Task Model

The Task model in `celery_worker_app` has the following fields:

- `id`: The Celery task ID
- `status`: Current status (PENDING, PROCESSING, DONE, FAILED)
- `task_name`: Name of the Celery task
- `created_at`: When the task was created
- `updated_at`: When the task was last updated
- `input_data`: JSON input data for the task
- `result`: JSON result data (including progress)
- `related_table`: Name of the table being operated on (e.g., "user")
- `related_id`: ID of the record being operated on
- `operation`: Type of operation (CREATE, READ, UPDATE, DELETE)

### User Model

The User model in `user_app` has the following fields:

- `id`: UUID primary key
- `username`: Unique username
- `email`: Unique email address
- `first_name`: First name
- `last_name`: Last name
- `is_active`: Whether the user is active
- `date_joined`: When the user was created