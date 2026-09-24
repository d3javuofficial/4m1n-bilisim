from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime

from backend.config import settings
from backend.database import get_db, engine, Base
from backend.models import Tender, TenderItem, Requirement, Supplier, AuditLog, ConnectionStatus
from backend.schemas import TenderCreate

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def setup_suppliers():
    db = next(get_db())
    suppliers_list = [
        ("PCBayi", "PCBayi B2B", "https://pcbayi.com"),
        ("BulutMarket", "Bulut Market B2B", "https://b2b.bulutmarket.com.tr"),
        ("Bilgisayarim", "Bilgisayarım", "https://bilgisayarim.com.tr"),
        ("eDenge", "eDenge", "https://edenge.com.tr"),
        ("Kamtek", "Kamtek Bayi", "https://bayi.kamtek.com.tr"),
        ("Arena", "Pencere / Arena B2B", "https://pencere.com"),
    ]
    for code, name, url in suppliers_list:
        if not db.query(Supplier).filter(Supplier.code == code).first():
            db.add(Supplier(code=code, name=name, base_url=url, connection_status=ConnectionStatus.NOT_CONFIGURED))
    db.commit()

@app.get("/api/v1/health")
def health():
    return {"status": "HEALTHY", "system": "4M1N Bilişim Teknolojileri"}

@app.get("/api/v1/dashboard/stats")
def get_stats(db: Session = Depends(get_db)):
    return {
        "total_tenders": db.query(Tender).count(),
        "analyzed_items": db.query(TenderItem).count(),
        "pass_count": 0,
        "manual_review_count": 0,
        "fail_count": 0,
        "total_suppliers": db.query(Supplier).count()
    }

@app.get("/api/v1/tenders")
def list_tenders(db: Session = Depends(get_db)):
    tenders = db.query(Tender).all()
    return [{
        "id": t.id,
        "tender_number": t.tender_number,
        "title": t.title,
        "institution": t.institution,
        "submission_deadline": t.submission_deadline.isoformat() if t.submission_deadline else "UNKNOWN",
        "item_count": len(t.items),
        "status": t.status
    } for t in tenders]

@app.post("/api/v1/tenders")
def create_tender(payload: TenderCreate, db: Session = Depends(get_db)):
    tender = Tender(
        tender_number=payload.tender_number,
        title=payload.title,
        institution=payload.institution,
        submission_deadline=payload.submission_deadline
    )
    db.add(tender)
    db.commit()
    db.refresh(tender)

    for item_data in payload.items:
        item = TenderItem(
            tender_id=tender.id,
            item_no=item_data.item_no,
            description=item_data.description,
            quantity=item_data.quantity,
            unit=item_data.unit
        )
        db.add(item)
        db.commit()
        db.refresh(item)

        for req_data in item_data.requirements:
            req = Requirement(
                item_id=item.id,
                field=req_data.field,
                operator=req_data.operator,
                value=req_data.value,
                unit=req_data.unit,
                mandatory=req_data.mandatory
            )
            db.add(req)

    log = AuditLog(user="4M1N Sistem", action="İHALE_OLUŞTURULDU", details=f"İhale No: {tender.tender_number}")
    db.add(log)
    db.commit()
    return {"status": "SUCCESS", "tender_id": tender.id}

@app.get("/api/v1/suppliers")
def list_suppliers(db: Session = Depends(get_db)):
    suppliers = db.query(Supplier).all()
    return [{
        "id": s.id,
        "code": s.code,
        "name": s.name,
        "base_url": s.base_url,
        "connection_status": s.connection_status.value,
        "last_check": s.last_check.isoformat() if s.last_check else "HENÜZ KONTROL EDİLMEDİ"
    } for s in suppliers]

@app.get("/api/v1/audit-logs")
def get_audit_logs(db: Session = Depends(get_db)):
    logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).all()
    return [{
        "id": l.id,
        "timestamp": l.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "user": l.user,
        "action": l.action,
        "details": l.details
    } for l in logs]