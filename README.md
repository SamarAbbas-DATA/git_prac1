FastAPI Blog API  
Small FastAPI project with a blog router (CRUD), basic user auth, and a scheduled cleanup job.

# Stack

FastAPI (+ Swagger UI at /docs)

MongoDB via pymongo

Pydantic models

passlib[bcrypt] for password hashing

APScheduler for background cleanup

Uvicorn server

## Project structure
project_root/
├─ blog/
│  ├─ __init__.py
│  ├─ main1.py          # FastAPI app entrypoint
│  ├─ database.py       # Mongo client + collections
│  ├─ schemas.py        # Pydantic models (Blog, User)
│  └─ auth.py           # JWT helpers
├─ routers/
│  ├─ __init__.py
│  └─ blogs.py          # /blogs router (CRUD)
└─ requirements.txt

# Quickstart

Prereqs: Python 3.10+ and MongoDB running locally.

1) Clone and enter
git clone <your-repo-url>
cd <repo-folder>

2) (Optional) create and activate venv
python -m venv venv
# Windows PowerShell:
.\venv\Scripts\Activate.ps1

3) Install deps
pip install -r requirements.txt
Tip (fixes spinning /docs on some systems):
pip install -U "fastapi[standard]" uvicorn

4) Run from the PROJECT ROOT (important)
uvicorn blog.main1:app --reload --host 127.0.0.1 --port 8001


API docs: http://127.0.0.1:8001/docs

# Environment

Default Mongo URL is in blog/database.py (mongodb://localhost:27017/).
You can switch to env variables if you want:

import os
MongoClient(os.getenv("MONGO_URL", "mongodb://localhost:27017/"))

# Endpoints (summary)

Blogs (routers/blogs.py, prefix /blogs):

GET /blogs – list all blogs

GET /blogs/get?title=... – find by title

POST /blogs – create a blog (adds created_at)

PUT /blogs/update?old_title=...&new_title=...&new_content=... – update

DELETE /blogs/delete?title=... – delete

Users (in main1.py):

- POST /users – create user (password hashed)

- GET /users?username=... – get users by username (password omitted)

Auth (in main1.py using auth.py):

- POST /login – returns JWT on valid creds

- GET /login – secured route (requires Authorization: Bearer <token>)

Dev notes

- Always run from project root: uvicorn blog.main1:app ...

- if /docs keeps spinning, install:
pip install -U "fastapi[standard]" and restart.

- APScheduler can double-start with --reload on Windows; if needed, start it inside FastAPI lifespan