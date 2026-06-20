from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from app.infrastructure.persistence.db import Base

class EventModel(Base):
    __tablename__ = "events"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    location: Mapped[str] = mapped_column(String, nullable=False)
    max_capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)

    categories: Mapped[list["TicketCategoryModel"]] = relationship("TicketCategoryModel", back_populates="event")

class TicketCategoryModel(Base):
    __tablename__ = "ticket_categories"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    event_id: Mapped[str] = mapped_column(String, ForeignKey("events.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    price_amount: Mapped[float] = mapped_column(Float, nullable=False)
    price_currency: Mapped[str] = mapped_column(String, default="IDR")
    quota: Mapped[int] = mapped_column(Integer, nullable=False)
    sales_start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    sales_end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    event: Mapped["EventModel"] = relationship("EventModel", back_populates="categories")

class BookingModel(Base):
    __tablename__ = "bookings"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    customer_id: Mapped[str] = mapped_column(String, nullable=False)
    event_id: Mapped[str] = mapped_column(String, nullable=False)
    category_id: Mapped[str] = mapped_column(String, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    total_price_amount: Mapped[float] = mapped_column(Float, nullable=False)
    total_price_currency: Mapped[str] = mapped_column(String, default="IDR")
    status: Mapped[str] = mapped_column(String, nullable=False)
    payment_deadline: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    tickets: Mapped[list["TicketModel"]] = relationship("TicketModel", back_populates="booking")

class TicketModel(Base):
    __tablename__ = "tickets"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    booking_id: Mapped[str] = mapped_column(String, ForeignKey("bookings.id"), nullable=False)
    code: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    checked_in_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    booking: Mapped["BookingModel"] = relationship("BookingModel", back_populates="tickets")

class RefundModel(Base):
    __tablename__ = "refunds"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    booking_id: Mapped[str] = mapped_column(String, nullable=False)
    customer_id: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    reason: Mapped[str | None] = mapped_column(String, nullable=True)
    rejection_reason: Mapped[str | None] = mapped_column(String, nullable=True)
    payment_reference: Mapped[str | None] = mapped_column(String, nullable=True)
    requested_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)