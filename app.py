from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import URL, AccessLog
from utils import generate_short_url, calculate_expiry, is_expired
from datetime import datetime

Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/shorten")
def shorten_url(original_url: str, expiry_hours: int = 24, db: Session = Depends(get_db)):
    short_id = generate_short_url(original_url)
    short_url = f"http://localhost:8000/{short_id}"

    existing = db.query(URL).filter(URL.short_url == short_id).first()
    if existing:
        return {"short_url": short_url, "expires_at": existing.expires_at}

    new_url = URL(
        original_url=original_url,
        short_url=short_id,
        expires_at=calculate_expiry(expiry_hours)
    )
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return {"short_url": short_url, "expires_at": new_url.expires_at}

@app.get("/{short_id}")
def redirect(short_id: str, request: Request, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.short_url == short_id).first()
    if not url or is_expired(url.expires_at):
        raise HTTPException(status_code=404, detail="URL expired or not found")

    log = AccessLog(short_url=short_id, ip_address=request.client.host)
    db.add(log)
    db.commit()
    return RedirectResponse(url.original_url)

@app.get("/analytics/{short_id}")
def analytics(short_id: str, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.short_url == short_id).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    logs = db.query(AccessLog).filter(AccessLog.short_url == short_id).all()
    return {
        "original_url": url.original_url,
        "short_url": url.short_url,
        "created_at": url.created_at,
        "expires_at": url.expires_at,
        "access_count": len(logs),
        "logs": [{"timestamp": log.timestamp, "ip": log.ip_address} for log in logs]
    }
