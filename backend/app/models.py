from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default='operator')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    waste_batches = relationship("WasteBatch", back_populates="user")

class WasteBatch(Base):
    __tablename__ = "waste_batches"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(String, unique=True, index=True)
    fabric_type = Column(String)
    source = Column(String)
    quantity_kg = Column(Float)
    color = Column(String)
    condition = Column(String)
    waste_category = Column(String)
    recyclability_score = Column(Float)
    contamination_level = Column(String, default='None')
    damage_level = Column(String, default='None')
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="waste_batches")
    analyses = relationship("TextileAnalysis", back_populates="batch")

class TextileAnalysis(Base):
    __tablename__ = "textile_analysis"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("waste_batches.id"))
    material_detected = Column(String)
    confidence = Column(Float)
    texture = Column(String)
    pattern = Column(String)
    fabric_color = Column(String)
    damage_level = Column(String)
    contamination_level = Column(String)
    reuse_potential = Column(String)
    disposal_recommendation = Column(String)
    recyclability_grade = Column(String, default='C')
    recyclability_score_computed = Column(Float, default=0.0)
    analyzed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    batch = relationship("WasteBatch", back_populates="analyses")

class CollectionRecord(Base):
    __tablename__ = "collection_records"

    id = Column(Integer, primary_key=True, index=True)
    source_name = Column(String)
    collection_date = Column(Date)
    total_weight_kg = Column(Float)
    items_count = Column(Integer)
    status = Column(String)
    collector_name = Column(String)
    notes = Column(Text, nullable=True)