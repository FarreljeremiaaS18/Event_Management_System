from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from app.presentation.request.booking_requests import CreateBookingRequest, PayBookingRequest
from app.application.booking.commands import CreateBookingCommand, PayBookingCommand
from app.application.booking.handlers import CreateBookingCommandHandler, PayBookingCommandHandler
from app.presentation.dependencies import get_create_booking_handler, get_pay_booking_handler

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/", status_code=201)
def create_booking(
    request: CreateBookingRequest,
    handler: CreateBookingCommandHandler = Depends(get_create_booking_handler)
):
    try:
        command = CreateBookingCommand(
            customer_id=request.customer_id,
            event_id=request.event_id,
            category_id=request.category_id,
            quantity=request.quantity,
            unit_price=request.unit_price
        )
        result_dto = handler.execute(command)
        return {"message": "Booking created successfully", "data": result_dto}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.post("/{booking_id}/pay")
def pay_booking(
    booking_id: UUID,
    request: PayBookingRequest,
    handler: PayBookingCommandHandler = Depends(get_pay_booking_handler)
):
    try:
        command = PayBookingCommand(
            booking_id=booking_id,
            payment_amount=request.payment_amount
        )
        result_dto = handler.execute(command)
        return {"message": "Payment successful", "data": result_dto}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))