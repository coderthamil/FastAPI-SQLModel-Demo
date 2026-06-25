
FASTAPI-SQLMODEL DEMO — README NOTES


# FastAPI-SQLModel Demo

This repository contains a simple demonstration of building a REST API using FastAPI and SQLModel.  
It shows how to define models, schemas, and CRUD routes for a basic Note resource.

--------------------------------------------------------
🚀 Features
--------------------------------------------------------
- FastAPI framework for high-performance APIs
- SQLModel for ORM + Pydantic validation
- SQLite database (easy to swap with PostgreSQL)
- Full CRUD operations:
  • Create a note
  • Read a note by ID
  • List all notes
  • Update a note
  • Delete a note
- Clear separation of ORM models and schemas

--------------------------------------------------------
📂 Project Structure
--------------------------------------------------------
FastAPI-SQLModel-demo/
│
├── main.py          # Application entry point
├── database.db      # SQLite database (auto-created)
└── README.txt       # Documentation

--------------------------------------------------------
🛠️ Setup Instructions
--------------------------------------------------------
1. Initialize project:
   uv init
   uv add fastapi sqlmodel psycopg2 uvicorn

2. Run the server:
   uvicorn main:app --reload

3. Open API docs:
   • Swagger UI → http://127.0.0.1:8000/docs
   • ReDoc → http://127.0.0.1:8000/redoc

--------------------------------------------------------
📑 Key Concepts
--------------------------------------------------------
ORM Model vs Schema
- ORM Model (Note, table=True)
  • Maps to a database table
  • Also acts as a Pydantic model
- Schema (NoteCreate, NoteUpdate, NoteRead)
  • Defines what the API expects and returns
  • Acts as a contract between client and server

👉 table=True is the “main switch” that makes a class persist in the database.

CRUD Operations
- Create → Convert schema → ORM with .model_validate(payload)
- Read by ID → session.get(Model, id)
- Read all → session.exec(select(Model)).all()
- Update → payload.dict(exclude_unset=True) ensures only provided fields are updated
- Delete → session.delete(existing)

--------------------------------------------------------
📘 Takeaways
--------------------------------------------------------
- Use table=True for ORM models (persisted in DB).
- Use plain SQLModel for schemas (API contracts).
- .dict() is critical:
  • .dict() → full payload
  • .dict(exclude_unset=True) → partial updates
- SQLModel combines SQLAlchemy ORM power with Pydantic validation, making it ideal for FastAPI projects.

--------------------------------------------------------
🔮 Next Steps
--------------------------------------------------------
- Swap SQLite for PostgreSQL by updating the create_engine connection string.
- Add authentication and role-based access.
- Extend with more models (e.g., Student, Employee, Product).
- Write unit tests for CRUD endpoints.

