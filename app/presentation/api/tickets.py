from fastapi import APIRouter, Depends, HTTPException
from app.presentation.request.ticket_requests import CheckInRequest
from app.application.ticket.commands import CheckInTicketCommand
from app.application.ticket.handlers import CheckInTicketCommandHandler
from app.presentation.dependencies import get_check_in_ticket_handler

router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.post("/{ticket_code}/check-in")
def check_in_ticket(
    ticket_code: str,
    request: CheckInRequest,
    handler: CheckInTicketCommandHandler = Depends(get_check_in_ticket_handler)
):
    try:
        command = CheckInTicketCommand(
            ticket_code=ticket_code,
            event_id=request.event_id
        )
        result = handler.execute(command)
        return {"message": "Ticket checked in successfully", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))