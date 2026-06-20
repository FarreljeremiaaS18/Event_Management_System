from fastapi import APIRouter, Depends, HTTPException
from app.presentation.request.event_requests import CreateEventRequest
from app.application.event.commands import CreateEventCommand
from app.application.event.handlers import CreateEventCommandHandler
from app.presentation.dependencies import get_create_event_handler


router = APIRouter(prefix="/events", tags=["Events"])

@router.post("/", status_code=201)
def create_event(
    request: CreateEventRequest,
    handler: CreateEventCommandHandler = Depends(get_create_event_handler)
):
    try:
        
        command = CreateEventCommand(
            name=request.name,
            description=request.description,
            start_date=request.start_date,
            end_date=request.end_date,
            location=request.location,
            max_capacity=request.max_capacity
        )
        
  
        result_dto = handler.execute(command)
        

        return {
            "message": "Event created successfully",
            "data": result_dto
        }
        
    except ValueError as e:
        
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
       
        raise HTTPException(status_code=422, detail=str(e))