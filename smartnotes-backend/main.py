from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import re
import time
import os

# ─────────────────────────────────────────────
# DATABASE SETUP
# ─────────────────────────────────────────────

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://smartnotes_user:smartnotes2024@localhost:5432/smartnotes")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ─────────────────────────────────────────────
# DATABASE MODELS
# ─────────────────────────────────────────────

class NoteModel(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    domain = Column(String, nullable=True)
    word_count = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    definitions = relationship("DefinitionModel", back_populates="note", cascade="all, delete-orphan")
    flashcards = relationship("FlashcardModel", back_populates="note", cascade="all, delete-orphan")


class DefinitionModel(Base):
    __tablename__ = "definitions"

    id = Column(Integer, primary_key=True, index=True)
    term = Column(String, nullable=False)
    meaning = Column(Text, nullable=False)
    domain = Column(String, nullable=True)
    confidence = Column(Float, nullable=True)
    pattern_used = Column(String, nullable=True)
    note_id = Column(Integer, ForeignKey("notes.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    note = relationship("NoteModel", back_populates="definitions")


class FlashcardModel(Base):
    __tablename__ = "flashcards"

    id = Column(Integer, primary_key=True, index=True)
    term = Column(String, nullable=False)
    definition = Column(Text, nullable=False)
    domain = Column(String, nullable=True)
    difficulty = Column(String, default="medium")
    times_reviewed = Column(Integer, default=0)
    times_correct = Column(Integer, default=0)
    next_review_at = Column(DateTime, default=datetime.utcnow)  # NEW
    interval_days = Column(Float, default=1.0)                  # NEW
    ease_factor = Column(Float, default=2.5)                    # NEW
    note_id = Column(Integer, ForeignKey("notes.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    note = relationship("NoteModel", back_populates="flashcards")


# Create all tables
Base.metadata.create_all(bind=engine)


# ─────────────────────────────────────────────
# PYDANTIC SCHEMAS
# ─────────────────────────────────────────────

class DefinitionOut(BaseModel):
    id: int
    term: str
    meaning: str
    domain: Optional[str]
    confidence: Optional[float]
    pattern_used: Optional[str]
    note_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class NoteOut(BaseModel):
    id: int
    filename: str
    domain: Optional[str]
    word_count: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


class NoteDetailOut(BaseModel):
    note: NoteOut
    definitions: List[DefinitionOut]
    definition_count: int


class ExtractResponse(BaseModel):
    note_id: int
    filename: str
    domain: str
    word_count: int
    definitions: List[DefinitionOut]
    definition_count: int
    flashcards_created: int
    processing_time_ms: float


class FlashcardOut(BaseModel):
    id: int
    term: str
    definition: str
    domain: Optional[str]
    difficulty: str
    times_reviewed: int
    times_correct: int
    next_review_at: datetime   # NEW
    interval_days: float       # NEW
    ease_factor: float         # NEW
    note_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class FlashcardReviewIn(BaseModel):
    quality: int  # 0=blackout, 1=wrong, 2=hard, 3=good, 4=easy, 5=perfect


# ─────────────────────────────────────────────
# DEPENDENCY: DB SESSION
# ─────────────────────────────────────────────

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ─────────────────────────────────────────────
# DEFINITION EXTRACTOR (21 patterns, 4 domains)
# ─────────────────────────────────────────────

DOMAIN_KEYWORDS = {
    "biology": [
        "cell", "organism", "dna", "rna", "protein", "enzyme", "mitosis", "meiosis",
        "photosynthesis", "respiration", "membrane", "nucleus", "chromosome", "gene",
        "evolution", "species", "metabolism", "homeostasis", "tissue", "organ"
    ],
    "history": [
        "war", "empire", "revolution", "treaty", "dynasty", "civilization", "colony",
        "democracy", "republic", "parliament", "monarchy", "industrial", "trade",
        "conquest", "nationalism", "imperialism", "reformation", "renaissance"
    ],
    "math": [
        "equation", "theorem", "proof", "function", "variable", "integer", "matrix",
        "vector", "derivative", "integral", "probability", "geometry", "algebra",
        "calculus", "polynomial", "coefficient", "axiom", "hypothesis", "formula"
    ],
    "literature": [
        "metaphor", "simile", "narrative", "protagonist", "antagonist", "theme",
        "symbolism", "irony", "alliteration", "sonnet", "prose", "stanza", "genre",
        "allegory", "foreshadowing", "characterization", "plot", "conflict"
    ]
}

PATTERNS = [
    {"name": "is_a_an", "regex": r"([A-Za-z][a-zA-Z\s\-]{1,40})\s+is\s+an?\s+([^.!?\n]{10,150})", "confidence": 0.90},
    {"name": "is_defined_as", "regex": r"([A-Za-z][a-zA-Z\s\-]{1,40})\s+is\s+defined\s+as\s+([^.!?\n]{10,150})", "confidence": 0.95},
    {"name": "refers_to", "regex": r"([A-Za-z][a-zA-Z\s\-]{1,40})\s+refers?\s+to\s+([^.!?\n]{10,150})", "confidence": 0.88},
    {"name": "means", "regex": r"([A-Za-z][a-zA-Z\s\-]{1,40})\s+means?\s+([^.!?\n]{10,150})", "confidence": 0.87},
    {"name": "colon_definition", "regex": r"^([A-Za-z][a-zA-Z\s\-]{1,40}):\s+([^.!?\n]{10,150})", "confidence": 0.85},
    {"name": "are_plural", "regex": r"([A-Za-z][a-zA-Z\s\-]{1,40})\s+are\s+([^.!?\n]{10,150})", "confidence": 0.82},
    {"name": "can_be_defined", "regex": r"([A-Za-z][a-zA-Z\s\-]{1,40})\s+can\s+be\s+defined\s+as\s+([^.!?\n]{10,150})", "confidence": 0.93},
    {"name": "is_the_process", "regex": r"([A-Za-z][a-zA-Z\s\-]{1,40})\s+is\s+the\s+process\s+of\s+([^.!?\n]{10,150})", "confidence": 0.91},
    {"name": "is_the_study", "regex": r"([A-Za-z][a-zA-Z\s\-]{1,40})\s+is\s+the\s+study\s+of\s+([^.!?\n]{10,150})", "confidence": 0.92},
    {"name": "is_known_as", "regex": r"([A-Za-z][a-zA-Z\s\-]{1,40})\s+is\s+known\s+as\s+([^.!?\n]{10,150})", "confidence": 0.86},
    {"name": "is_called", "regex": r"([A-Za-z][a-zA-Z\s\-]{1,40})\s+is\s+(?:also\s+)?called\s+([^.!?\n]{10,150})", "confidence": 0.84},
    {"name": "describes", "regex": r"([A-Za-z][a-zA-Z\s\-]{1,40})\s+describes?\s+([^.!?\n]{10,150})", "confidence": 0.83},
    {"name": "involves", "regex": r"([A-Za-z][a-zA-Z\s\-]{1,40})\s+involves?\s+([^.!?\n]{10,150})", "confidence": 0.80},
    {"name": "consists_of", "regex": r"([A-Za-z][a-zA-Z\s\-]{1,40})\s+consists?\s+of\s+([^.!?\n]{10,150})", "confidence": 0.81},
    {"name": "represents", "regex": r"([A-Za-z][a-zA-Z\s\-]{1,40})\s+represents?\s+([^.!?\n]{10,150})", "confidence": 0.79},
    {"name": "the_term_means", "regex": r"[Tt]he\s+term\s+['\"]?([A-Za-z\s\-]{2,40})['\"]?\s+means?\s+([^.!?\n]{10,150})", "confidence": 0.94},
    {"name": "domain_context", "regex": r"[Ii]n\s+\w+,?\s+([A-Za-z][a-zA-Z\s\-]{1,40})\s+is\s+([^.!?\n]{10,150})", "confidence": 0.88},
    {"name": "was_a_an", "regex": r"([A-Za-z][a-zA-Z\s\-]{1,40})\s+was\s+an?\s+([^.!?\n]{10,150})", "confidence": 0.85},
    {"name": "were_plural", "regex": r"([A-Za-z][a-zA-Z\s\-]{1,40})\s+were\s+([^.!?\n]{10,150})", "confidence": 0.82},
    {"name": "dash_definition", "regex": r"^([A-Za-z][a-zA-Z\s\-]{1,40})\s+[-–]\s+([^.!?\n]{10,150})", "confidence": 0.83},
    {"name": "action_definition", "regex": r"([A-Za-z][a-zA-Z\s\-]{1,40})\s+wanted\s+to\s+([^.!?\n]{10,150})", "confidence": 0.75},
]


def detect_domain(text: str) -> str:
    text_lower = text.lower()
    scores = {domain: 0 for domain in DOMAIN_KEYWORDS}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                scores[domain] += 1
    best_domain = max(scores, key=scores.get)
    if scores[best_domain] < 2:
        return "general"
    return best_domain


def extract_definitions(text: str, domain: str) -> list:
    found = []
    seen_terms = set()
    for pattern in PATTERNS:
        matches = re.finditer(pattern["regex"], text, re.MULTILINE)
        for match in matches:
            term = match.group(1).strip()
            meaning = match.group(2).strip()
            term = re.sub(r'\s+', ' ', term).strip(".,;: ")
            meaning = re.sub(r'\s+', ' ', meaning).strip(".,;: ")
            STOPWORDS = {"they", "them", "which", "this", "that", "these", "those",
             "it", "he", "she", "we", "you", "i", "who", "what",
             "most of them", "some of them", "all of them", "there"}

            BAD_STARTS = ("by ", "in ", "of ", "to ", "the ", "a ", "an ", "and ", "or ", "for ", "on ")
            if len(term) < 2 or term.lower() in seen_terms:
                continue
            if term.lower() in STOPWORDS:
                continue
            if any(term.lower().startswith(s) for s in BAD_STARTS):
                continue
            seen_terms.add(term.lower())
            found.append({
                "term": term,
                "meaning": meaning,
                "domain": domain,
                "confidence": pattern["confidence"],
                "pattern_used": pattern["name"]
            })
    return found


# ─────────────────────────────────────────────
# FASTAPI APP
# ─────────────────────────────────────────────

app = FastAPI(
    title="SmartNotes API",
    description="AI-powered definition extraction from student notes",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────────
# ENDPOINTS
# ─────────────────────────────────────────────

@app.get("/", tags=["Health"])
def root():
    return {"message": "SmartNotes API is running 🚀", "version": "1.0.0", "docs": "/docs"}


@app.get("/api/health", tags=["Health"])
def health_check(db: Session = Depends(get_db)):
    try:
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    return {"status": "ok", "database": db_status, "timestamp": datetime.utcnow().isoformat()}


@app.post("/api/extract", response_model=ExtractResponse, tags=["Extraction"])
async def extract_definitions_endpoint(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload a .txt note file — extracts definitions and auto-generates flashcards."""
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are supported")

    start_time = time.time()
    content_bytes = await file.read()
    content = content_bytes.decode("utf-8")

    if not content.strip():
        raise HTTPException(status_code=400, detail="File is empty")

    domain = detect_domain(content)
    extracted = extract_definitions(content, domain)
    word_count = len(content.split())

    # Save note
    note = NoteModel(filename=file.filename, content=content, domain=domain, word_count=word_count)
    db.add(note)
    db.flush()

    # Save definitions
    saved_definitions = []
    for defn in extracted:
        record = DefinitionModel(
            term=defn["term"],
            meaning=defn["meaning"],
            domain=defn["domain"],
            confidence=defn["confidence"],
            pattern_used=defn["pattern_used"],
            note_id=note.id
        )
        db.add(record)
        saved_definitions.append(record)

    db.flush()

    # Auto-generate flashcards from definitions
    flashcards_created = []
    for defn in saved_definitions:
        flashcard = FlashcardModel(
            term=defn.term,
            definition=defn.meaning,
            domain=defn.domain,
            difficulty="medium",
            note_id=note.id
        )
        db.add(flashcard)
        flashcards_created.append(flashcard)

    db.commit()

    db.refresh(note)
    for record in saved_definitions:
        db.refresh(record)
    for fc in flashcards_created:
        db.refresh(fc)

    processing_time = (time.time() - start_time) * 1000

    return ExtractResponse(
        note_id=note.id,
        filename=note.filename,
        domain=domain,
        word_count=word_count,
        definitions=[DefinitionOut.from_orm(d) for d in saved_definitions],
        definition_count=len(saved_definitions),
        flashcards_created=len(flashcards_created),
        processing_time_ms=round(processing_time, 2)
    )


@app.get("/api/notes", tags=["Notes"])
def list_notes(db: Session = Depends(get_db)):
    notes = db.query(NoteModel).order_by(NoteModel.created_at.desc()).all()
    return {"notes": [NoteOut.from_orm(n) for n in notes], "count": len(notes)}


@app.get("/api/notes/{note_id}", response_model=NoteDetailOut, tags=["Notes"])
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(NoteModel).filter(NoteModel.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail=f"Note {note_id} not found")
    definitions = db.query(DefinitionModel).filter(DefinitionModel.note_id == note_id).all()
    return NoteDetailOut(
        note=NoteOut.from_orm(note),
        definitions=[DefinitionOut.from_orm(d) for d in definitions],
        definition_count=len(definitions)
    )


@app.delete("/api/notes/{note_id}", tags=["Notes"])
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(NoteModel).filter(NoteModel.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail=f"Note {note_id} not found")
    definition_count = db.query(DefinitionModel).filter(DefinitionModel.note_id == note_id).count()
    flashcard_count = db.query(FlashcardModel).filter(FlashcardModel.note_id == note_id).count()
    db.delete(note)
    db.commit()
    return {"message": f"Note {note_id} deleted", "definitions_removed": definition_count, "flashcards_removed": flashcard_count}


@app.get("/api/definitions", tags=["Definitions"])
def list_all_definitions(domain: Optional[str] = None, limit: int = 50, db: Session = Depends(get_db)):
    query = db.query(DefinitionModel)
    if domain:
        query = query.filter(DefinitionModel.domain == domain)
    definitions = query.order_by(DefinitionModel.created_at.desc()).limit(limit).all()
    return {"definitions": [DefinitionOut.from_orm(d) for d in definitions], "count": len(definitions), "filter_domain": domain}


@app.get("/api/flashcards", tags=["Flashcards"])
def list_flashcards(domain: Optional[str] = None, difficulty: Optional[str] = None, limit: int = 20, db: Session = Depends(get_db)):
    """Get flashcards to study. Filter by domain or difficulty."""
    query = db.query(FlashcardModel)
    if domain:
        query = query.filter(FlashcardModel.domain == domain)
    if difficulty:
        query = query.filter(FlashcardModel.difficulty == difficulty)
    flashcards = query.order_by(FlashcardModel.created_at.desc()).limit(limit).all()
    return {"flashcards": [FlashcardOut.from_orm(f) for f in flashcards], "count": len(flashcards)}


@app.get("/api/flashcards/note/{note_id}", tags=["Flashcards"])
def get_flashcards_for_note(note_id: int, db: Session = Depends(get_db)):
    """Get all flashcards generated from a specific note."""
    flashcards = db.query(FlashcardModel).filter(FlashcardModel.note_id == note_id).all()
    return {"flashcards": [FlashcardOut.from_orm(f) for f in flashcards], "count": len(flashcards), "note_id": note_id}


@app.post("/api/flashcards/{flashcard_id}/review", tags=["Flashcards"])
def review_flashcard(flashcard_id: int, review: FlashcardReviewIn, db: Session = Depends(get_db)):
    """
    SM-2 spaced repetition algorithm.
    quality: 0=blackout, 1=wrong, 2=hard, 3=good, 4=easy, 5=perfect
    """
    from datetime import timedelta

    fc = db.query(FlashcardModel).filter(FlashcardModel.id == flashcard_id).first()
    if not fc:
        raise HTTPException(status_code=404, detail="Flashcard not found")

    q = max(0, min(5, review.quality))  # clamp to 0-5

    fc.times_reviewed += 1
    if q >= 3:
        fc.times_correct += 1

    # ── SM-2 Algorithm ──
    if q < 2:
        # Failed — reset interval
        fc.interval_days = 1
    elif fc.times_reviewed == 1:
        fc.interval_days = 1
    elif fc.times_reviewed == 2:
        fc.interval_days = 6
    else:
        fc.interval_days = round(fc.interval_days * fc.ease_factor, 1)

    # Update ease factor (stays between 1.3 and 2.5)
    fc.ease_factor = max(1.3, fc.ease_factor + 0.1 - (5 - q) * 0.08)

    # Schedule next review
    fc.next_review_at = datetime.utcnow() + timedelta(days=fc.interval_days)

    # Update difficulty label
    if fc.ease_factor >= 2.3:
        fc.difficulty = "easy"
    elif fc.ease_factor >= 1.8:
        fc.difficulty = "medium"
    else:
        fc.difficulty = "hard"

    db.commit()
    db.refresh(fc)

    return {
        "flashcard_id": flashcard_id,
        "quality": q,
        "new_interval_days": fc.interval_days,
        "next_review_at": fc.next_review_at.isoformat(),
        "ease_factor": round(fc.ease_factor, 2),
        "difficulty": fc.difficulty
    }


@app.get("/api/study/session", tags=["Flashcards"])
def get_study_session(domain: Optional[str] = None, count: int = 10, db: Session = Depends(get_db)):
    """
    Smart study session: due cards first, then hard, then medium, then easy.
    """
    from datetime import timedelta
    now = datetime.utcnow()

    def get_cards(difficulty, limit):
        query = db.query(FlashcardModel).filter(FlashcardModel.difficulty == difficulty)
        if domain:
            query = query.filter(FlashcardModel.domain == domain)
        return query.limit(limit).all()

    # Due cards take absolute priority
    due_query = db.query(FlashcardModel).filter(FlashcardModel.next_review_at <= now)
    if domain:
        due_query = due_query.filter(FlashcardModel.domain == domain)
    due = due_query.order_by(FlashcardModel.next_review_at.asc()).limit(count).all()

    session_cards = list(due)

    # Fill remaining slots with hard → medium → easy
    if len(session_cards) < count:
        for difficulty in ["hard", "medium", "easy"]:
            for card in get_cards(difficulty, count):
                if len(session_cards) >= count:
                    break
                if card not in session_cards:
                    session_cards.append(card)

    return {
        "session_cards": [FlashcardOut.from_orm(f) for f in session_cards],
        "count": len(session_cards),
        "due_count": len(due),
        "domain": domain,
        "priority_order": "due → hard → medium → easy"
    }


@app.get("/api/stats", tags=["Analytics"])
def get_stats(db: Session = Depends(get_db)):
    total_notes = db.query(NoteModel).count()
    total_definitions = db.query(DefinitionModel).count()
    total_flashcards = db.query(FlashcardModel).count()

    domain_breakdown = {}
    for domain in ["biology", "history", "math", "literature", "general"]:
        domain_breakdown[domain] = db.query(DefinitionModel).filter(DefinitionModel.domain == domain).count()

    all_defs = db.query(DefinitionModel).all()
    avg_conf = round(sum(d.confidence for d in all_defs) / len(all_defs), 3) if all_defs else 0

    return {
        "total_notes": total_notes,
        "total_definitions": total_definitions,
        "total_flashcards": total_flashcards,
        "average_confidence": avg_conf,
        "domain_breakdown": domain_breakdown,
        "patterns_available": len(PATTERNS),
        "domains_supported": list(DOMAIN_KEYWORDS.keys())
    }

@app.get("/api/study/due", tags=["Flashcards"])
def get_due_cards(domain: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Returns all flashcards due for review right now.
    This is the spaced repetition scheduler.
    """
    from datetime import timedelta
    now = datetime.utcnow()

    query = db.query(FlashcardModel).filter(
        FlashcardModel.next_review_at <= now
    )
    if domain:
        query = query.filter(FlashcardModel.domain == domain)

    due_cards = query.order_by(FlashcardModel.next_review_at.asc()).all()

    return {
        "due_cards": [FlashcardOut.from_orm(f) for f in due_cards],
        "due_count": len(due_cards),
        "checked_at": now.isoformat(),
        "message": f"{len(due_cards)} cards due for review"
    }