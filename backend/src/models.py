from pydantic import BaseModel, Field, field_validator
from src.utils import PyObjectId, validate_object_id
from typing import Union
from bson import ObjectId
from datetime import datetime
from typing import Any



# Room models

class Room(BaseModel):
    id: Union[PyObjectId, None] = Field(alias='_id', default=None)
    name: str
    devices: Union[list["Device"], None] = None
    sensors: Union[list["Sensor"], None] = None
    temperature: Union[float, None] = None


class RoomCreate(BaseModel):
    name: str = Field(..., example="Living Room")

class RoomUpdate(BaseModel):
    name: Union[str, None] = Field(None, example="Living Room")


class RoomDeviceSummary(BaseModel):
    room: Room
    devices: list["Device"]

class RoomActivity(BaseModel):
    activity_id : PyObjectId
    device_name: str
    device_type: str
    device_model: str
    timestamp: datetime
    activity: str
    device_id: PyObjectId


class RoomConsumption(BaseModel):
    device_id: PyObjectId
    consumption_id: PyObjectId
    device_name: str
    device_type: str
    device_model: str
    device_consumption: float 
    timestamp: datetime


# Device models

class Device(BaseModel):
    id: Union[PyObjectId, None] = Field(alias='_id', default=None)
    name: str
    type: str = Field(..., example="Fridge")
    model: str = Field(..., example="Samsung")
    room_id: PyObjectId
    status: str = Field(..., example="off")
    activities: Union[list["DeviceActivity"], None] = None
    consumption: Union[list["DeviceConsumption"], None] = None
    room: Union["Room", None] = None
    total_consumption: Union[float, None] = None

class DeviceCreate(BaseModel):
    type: str = Field(..., example="Fridge")
    name: str = Field(..., example="Living Room Fridge")
    model: str = Field(..., example="Samsung")
    room_id: PyObjectId
    status: str = Field(..., example="off")

    _validate_object_id = field_validator('room_id')(validate_object_id)

class DeviceUpdate(BaseModel):
    name: Union[str, None] = Field(None, example="Living Room Fridge")
    type: Union[str, None] = Field(None, example="Fridge")
    model: Union[str, None] = Field(None, example="Samsung")
    room_id: Union[PyObjectId, None] = None

    _validate_object_id = field_validator('room_id')(validate_object_id)


class DeviceActivity(BaseModel):
    id: Union[PyObjectId, None] = Field(alias='_id', default=None)
    activity: str
    timestamp: datetime

class DeviceConsumption(BaseModel):
    id: Union[PyObjectId, None] = Field(alias='_id', default=None)
    timestamp: datetime
    value: float


# Sensor models

class Sensor(BaseModel):
    id: Union[PyObjectId, None] = Field(alias='_id', default=None)
    type: str = Field(..., example="Temperature")
    room_id: PyObjectId
    readings: Union[list["SensorReading"], None] = None


class SensorCreate(BaseModel):
    type: str = Field(..., example="Temperature")
    room_id: PyObjectId

    _validate_object_id = field_validator('room_id')(validate_object_id)

class SensorUpdate(BaseModel):
    type: Union[str, None] = Field(None, example="Temperature")
    room_id: Union[PyObjectId, None] = None

    _validate_object_id = field_validator('room_id')(validate_object_id)

class SensorReading(BaseModel):
    id: Union[PyObjectId, None] = Field(alias='_id', default=None)
    timestamp: datetime
    value: Any
