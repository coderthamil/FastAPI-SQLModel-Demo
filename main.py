from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Field, Session, create_engine, select
from datetime import datetime
from typing import Optional

# -----------------------------
# 1. ORM Model (Database Table)
# -----------------------------
class Note(SQLModel, table=True):
    """
    ORM model that defines the 'notes' table in the database.
    Includes DB-managed fields like id and created_at.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    is_published: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


# -----------------------------
# 2. Schemas (API Contracts)
# -----------------------------
class NoteCreate(SQLModel):
    """
    Schema for creating a new note.
    Excludes DB-managed fields like id and created_at.
    """
    title: str
    content: str
    is_published: bool = False


class NoteUpdate(SQLModel):
    """
    Schema for updating a note.
    All fields optional so partial updates are possible.
    """
    title: Optional[str] = None
    content: Optional[str] = None
    is_published: Optional[bool] = None


class NoteRead(SQLModel):
    """
    Schema for reading a note.
    Defines what is returned to the client.
    """
    id: int
    title: str
    content: str
    is_published: bool
    created_at: datetime


# -----------------------------
# 3. FastAPI App + Database
# -----------------------------
app = FastAPI(title="Notes API with SQLModel")
engine = create_engine("sqlite:///database.db", echo=True)
'''engine = create_engine(
    "postgresql+psycopg2://notes_user:yourpassword@localhost:5432/notes_db",
    echo=True
)
'''
@app.on_event("startup")
def on_startup():
    """
    Runs when the app starts.
    Creates tables if they don't exist.
    """
    SQLModel.metadata.create_all(engine)

def get_session():
    """
    Dependency that provides a database session.
    Ensures clean session handling per request.
    """
    with Session(engine) as session:
        yield session


# -----------------------------
# 4. CRUD Routes
# -----------------------------

# Create
@app.post("/notes/", response_model=NoteRead)
def create_note(payload: NoteCreate, session: Session = Depends(get_session)):
    """
    Create a new note from client payload.
    Converts NoteCreate schema → ORM Note model using model_validate().
    """
    db_note = Note.model_validate(payload)   # Convert schema → ORM model
    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    return db_note


# Read by ID
@app.get("/notes/{note_id}", response_model=NoteRead)
def read_note(note_id: int, session: Session = Depends(get_session)):
    """
    Fetch a single note by ID.
    Returns 404 if not found.
    """
    db_note = session.get(Note, note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note


# Read all
@app.get("/notes/", response_model=list[NoteRead])
def list_notes(session: Session = Depends(get_session)):
    """
    Fetch all notes from the database.
    """
    notes = session.exec(select(Note)).all()
    return notes


# Update
@app.put("/notes/{note_id}", response_model=NoteRead)
def update_note(note_id: int, payload: NoteUpdate, session: Session = Depends(get_session)):
    """
    Update an existing note.
    Uses dict(exclude_unset=True) to apply only provided fields.
    """
    db_note = session.get(Note, note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")

    for key, value in payload.dict(exclude_unset=True).items():
        setattr(db_note, key, value)

    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    return db_note


# Delete
@app.delete("/notes/{note_id}")
def delete_note(note_id: int, session: Session = Depends(get_session)):
    """
    Delete a note by ID.
    Returns success message if deleted.
    """
    db_note = session.get(Note, note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")

    session.delete(db_note)
    session.commit()
    return {"detail": "Note deleted successfully"}
