from fastapi import FastAPI
from app.presentation.api import events, bookings



app = FastAPI(
    title="Event Management System API",
    description="REST API for managing events, bookings, and refunds.",
    version="1.0.0"
)


app.include_router(events.router)
app.include_router(bookings.router)

@app.get("/")
def root():
    return {"message": "Welcome to Event Management System API"}