from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from datetime import date
from typing import List

app = FastAPI()

# Data Model
class Event(BaseModel):
    id: int
    title: str
    date: date
    description: str

    @field_validator('date')
    @classmethod
    def date_must_not_be_past(cls, v):
        if v < date.today():
            raise ValueError('Date cannot be in the past')
        return v

# In-memory database
events_db = []

@app.get("/events", response_model=List[Event])
def get_events():
    # Sort events by date before returning
    return sorted(events_db, key=lambda x: x.date)

@app.post("/events")
def create_event(event: Event):
    # Check if ID already exists
    if any(e.id == event.id for e in events_db):
        raise HTTPException(status_code=400, detail="Event ID already exists")
    
    events_db.append(event)
    return {"message": "Event added successfully", "event": event}

@app.delete("/events/{event_id}")
def delete_event(event_id: int):
    global events_db
    events_db = [e for e in events_db if e.id != event_id]
    return {"message": "Event deleted successfully"}

@app.put("/events/{event_id}")
def update_event(event_id: int, updated_event: Event):
    for index, event in enumerate(events_db):
        if event.id == event_id:
            events_db[index] = updated_event
            return {"message": "Event updated successfully", "event": updated_event}
    
    raise HTTPException(status_code=404, detail="Event not found")
