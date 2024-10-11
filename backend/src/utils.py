from pydantic import BeforeValidator
from typing import Annotated
from bson import ObjectId
from fastapi import HTTPException

PyObjectId = Annotated[str, BeforeValidator(str)]

def validate_object_id(value: str) -> str:
    if not ObjectId.is_valid(value):
        raise ValueError("Invalid ObjectId")
    return value


def check_valid_room(room_id: str, db):
    oid = ObjectId(room_id)
    room = db.rooms.find_one({'_id': oid})
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    
    return oid 