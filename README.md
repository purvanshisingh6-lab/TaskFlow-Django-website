# Task Manager Website

A Django-based task management website with user registration, login/logout, and personal task tracking.

## Features
- User registration and login
- Add, edit, delete, and complete tasks
- Each user sees only their own tasks
- Search tasks by title or description
- Filter tasks: All, Pending, Completed
- Responsive layout
- SQLite database for local development

## Requirements
- Python 3.10+
- pip

## Run locally (Windows)
Open a terminal in this project folder and run:

```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

Create an admin account if needed:
```powershell
python manage.py createsuperuser
```
Then open http://127.0.0.1:8000/admin/.

## GitHub upload
1. Extract this ZIP.
2. Open the extracted `task_manager_website` folder in VS Code.
3. Test it using the commands above.
4. In GitHub, create a new empty repository.
5. In VS Code, use Source Control to initialize Git, commit the files, and publish the branch; or use GitHub Desktop.
6. Do not upload your `.venv`, `.env`, or `db.sqlite3`.

## Deployment note
This starter is configured for local development (`DEBUG=True`) and SQLite. Before deploying publicly, set `DEBUG=False`, configure `ALLOWED_HOSTS`, use environment variables for `SECRET_KEY`, and choose a production database/server.
