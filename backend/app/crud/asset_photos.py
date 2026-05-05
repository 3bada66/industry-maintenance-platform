# backend/crud/asset_photos.py
from sqlalchemy.orm import Session
from app.models import AssetPhoto
from app.schemas import AssetPhotoCreate
import uuid


def create_asset_photo(db: Session, photo: AssetPhotoCreate) -> AssetPhoto:
    db_photo = AssetPhoto(
        id=uuid.uuid4(), asset_id=photo.asset_id, file_path=photo.file_path
    )
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    return db_photo


def get_asset_photos(db: Session, asset_id: uuid.UUID) -> list[AssetPhoto]:
    return db.query(AssetPhoto).filter(AssetPhoto.asset_id == asset_id).all()


def delete_asset_photo(db: Session, photo_id: uuid.UUID):
    photo = db.query(AssetPhoto).filter(AssetPhoto.id == photo_id).first()
    if photo:
        db.delete(photo)
        db.commit()
