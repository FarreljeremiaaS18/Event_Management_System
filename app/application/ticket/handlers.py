from app.application.ticket.commands import CheckInTicketCommand, TicketDTO
from app.domain.ticket.repository import ITicketRepository 

class CheckInTicketCommandHandler:
    def __init__(self, repository: ITicketRepository):
        self.repository = repository

    def execute(self, command: CheckInTicketCommand) -> TicketDTO:
        ticket = self.repository.find_by_code(command.ticket_code)
        
        if ticket.event_id != command.event_id:
            raise ValueError("Tiket tidak sesuai dengan acara ini")
            
        ticket.check_in()
        self.repository.save(ticket)
        return TicketDTO(ticket_code=ticket.ticket_code, status=ticket.status.value)