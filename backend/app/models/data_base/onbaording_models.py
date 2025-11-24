from sqlalchemy import String, DateTime, Integer, Text, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from typing import Optional

Base = declarative_base()

class VerificationStatusModel(Base): 
    __tablename__ = "verification_status"  
    __table_args__ = {"schema": "public"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(50))  
    description: Mapped[str] = mapped_column(String(255)) 

    verification_requests: Mapped[list["VerificationRequestModel"]] = relationship(
        "VerificationRequestModel", 
        back_populates="status_ref"
    )

class DocumentTypeModel(Base):
    __tablename__ = "document_type"
    __table_args__ = {"schema": "public"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(255))  

    verification_requests: Mapped[list["VerificationRequestModel"]] = relationship(
        "VerificationRequestModel", 
        back_populates="document_type_ref"
    )

class RiskLevelCatalogModel(Base):  
    __tablename__ = "risk_level_catalog"  
    __table_args__ = {"schema": "public"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(20))  
    description: Mapped[str] = mapped_column(String(255)) 

    verification_requests: Mapped[list["VerificationRequestModel"]] = relationship(
        "VerificationRequestModel", 
        back_populates="risk_level_ref"
    )

class CountryCatalogModel(Base):
    __tablename__ = "country_catalog"
    __table_args__ = {"schema": "public"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    calling_code: Mapped[str] = mapped_column(String(10), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    verification_requests: Mapped[list["VerificationRequestModel"]] = relationship(
        "VerificationRequestModel", 
        back_populates="country_ref"
    )

class VerificationRequestModel(Base):
    __tablename__ = "verification_requests"
    __table_args__ = {"schema": "public"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(50))
    country_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("public.country_catalog.id")
    )
    document_type_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("public.document_type.id")
    )
    document_number: Mapped[str] = mapped_column(String(100))
    document_image_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  
    selfie_image_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  
    status_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("public.verification_status.id") 
    )
    risk_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    risk_level_id: Mapped[uuid.UUID] = mapped_column(  
        UUID(as_uuid=True), ForeignKey("public.risk_level_catalog.id")  
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    status_ref: Mapped["VerificationStatusModel"] = relationship( 
        "VerificationStatusModel", 
        back_populates="verification_requests",
        foreign_keys=[status_id]
    )
    
    document_type_ref: Mapped["DocumentTypeModel"] = relationship(
        "DocumentTypeModel", 
        back_populates="verification_requests",
        foreign_keys=[document_type_id]
    )
    
    risk_level_ref: Mapped["RiskLevelCatalogModel"] = relationship( 
        "RiskLevelCatalogModel",
        back_populates="verification_requests",
        foreign_keys=[risk_level_id]
    )
    
    country_ref: Mapped["CountryCatalogModel"] = relationship( 
        "CountryCatalogModel",
        back_populates="verification_requests",
        foreign_keys=[country_id]
    )

class VerificationRequestViewModel(Base):  
    __tablename__ = "vw_verification_requests"
    __table_args__ = {"schema": "public"}

    __mapper_args__ = {
        "primary_key": ["id"],
        "concrete": True
    }
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(50))
    country: Mapped[str] = mapped_column(String(100))
    country_calling_code: Mapped[str] = mapped_column(String(10)) 
    document_type: Mapped[str] = mapped_column(String(100))
    document_number: Mapped[str] = mapped_column(String(100))
    document_image_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True) 
    selfie_image_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  
    status: Mapped[str] = mapped_column(String(50))
    risk_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    risk_level: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime)