import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.infra.postgresql.postgres_base_model import PostgresBaseModel

class VerificationRequestModel(PostgresBaseModel):
    __tablename__ = "verification_requests"
    __table_args__ = {"schema": "public"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    full_name: Mapped[str]
    email: Mapped[str]
    phone: Mapped[str]
    country: Mapped[str]
    document_type: Mapped[str]
    document_number: Mapped[str]

    document_image_url: Mapped[str | None]
    selfie_image_url: Mapped[str | None]

    status: Mapped[str] = mapped_column(default="pending")

    risk_score: Mapped[int | None]
    risk_level: Mapped[str | None]

    created_at: Mapped[datetime] = mapped_column()
    updated_at: Mapped[datetime] = mapped_column()
