from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.infrastructure.persistence.db import Base

class EventModel(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)
    max_capacity = Column(Integer, nullable=False)
    status = Column(String, nullable=False)

    categories = relationship("TicketCategoryModel", back_populates="event")

class TicketCategoryModel(Base):
    __tablename__ = "ticket_categories"

    id = Column(String, primary_key=True, index=True)
    event_id = Column(String, ForeignKey("events.id"), nullable=False)
    name = Column(String, nullable=False)
    price_amount = Column(Float, nullable=False)
    price_currency = Column(String, default="IDR")
    quota = Column(Integer, nullable=False)
    sales_start_date = Column(DateTime, nullable=False)
    sales_end_date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)

    event = relationship("EventModel", back_populates="categories")

class BookingModel(Base):
    __tablename__ = "bookings"

    id = Column(String, primary_key=True, index=True)
    customer_id = Column(String, nullable=False)
    event_id = Column(String, nullable=False)
    category_id = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price_amount = Column(Float, nullable=False)
    total_price_currency = Column(String, default="IDR")
    status = Column(String, nullable=False)
    payment_deadline = Column(DateTime)

    tickets = relationship("TicketModel", back_populates="booking")

class TicketModel(Base):
    __tablename__ = "tickets"

    id = Column(String, primary_key=True, index=True)
    booking_id = Column(String, ForeignKey("bookings.id"), nullable=False)
    code = Column(String, unique=True, index=True, nullable=False)
    status = Column(String, nullable=False)
    checked_in_at = Column(DateTime, nullable=True)

    booking = relationship("BookingModel", back_populates="tickets")

class RefundModel(Base):
    __tablename__ = "refunds"

    id = Column(String, primary_key=True, index=True)
    booking_id = Column(String, nullable=False)
    customer_id = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, nullable=False)
    reason = Column(String, nullable=True)
    rejection_reason = Column(String, nullable=True)
    payment_reference = Column(String, nullable=True)
    requested_at = Column(DateTime, nullable=False)