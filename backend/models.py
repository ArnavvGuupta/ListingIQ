
from sqlalchemy import Column, BigInteger, String, Text, TIMESTAMP, text, Index

from database import Base


class Listing(Base):
    __tablename__ = "listing_master"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    business_name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=True)
    city = Column(String(100), nullable=False)
    address = Column(Text, nullable=True)
    phone = Column(String(30), nullable=True)
    source = Column(String(50), nullable=False)
    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
    )

    __table_args__ = (
        Index("idx_city", "city"),
        Index("idx_category", "category"),
        Index("idx_source", "source"),
    )
