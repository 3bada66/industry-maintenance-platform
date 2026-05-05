# backend/crud/asset_documents.py
from sqlalchemy.orm import Session
from app.models import AssetDocument
from app.schemas import AssetDocumentCreate
import uuid


def create_asset_document(db: Session, doc: AssetDocumentCreate) -> AssetDocument:
    db_doc = AssetDocument(
        id=uuid.uuid4(),
        asset_id=doc.asset_id,
        name=doc.name,
        description=doc.description,
        tenant_id=doc.tenant_id,
        file_path=doc.file_path,
    )
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc


def get_asset_documents(db: Session, asset_id: uuid.UUID) -> list[AssetDocument]:
    return db.query(AssetDocument).filter(AssetDocument.asset_id == asset_id).all()


def delete_asset_document(db: Session, doc_id: uuid.UUID):
    doc = db.query(AssetDocument).filter(AssetDocument.id == doc_id).first()
    if doc:
        db.delete(doc)
        db.commit()
