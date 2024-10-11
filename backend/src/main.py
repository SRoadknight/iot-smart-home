from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel, BeforeValidator, Field
from typing import Annotated, Union
from contextlib import asynccontextmanager
from logging import info
import src.service as service
from src.models import (
    Room, 
    RoomCreate, 
    RoomUpdate,
    Device,
    DeviceCreate,
    DeviceUpdate,
    Sensor,
    SensorCreate,
    SensorUpdate,
    RoomActivity
)



@asynccontextmanager
async def db_lifespan(app: FastAPI):
    app.mongodb_client = MongoClient("mongodb://iot_home_web:iot_home_web@mongo1:27017,mongo2:27018,mongo3:27019/?replicaSet=rs0")
    app.database = app.mongodb_client.get_database('iot_home')
    ping_response = app.database.command("ping")
    if int(ping_response.get("ok")) != 1:
        raise ValueError("Could not connect to database")
    else:
        info(f"Connected to database: {app.database.name}")

    yield

    app.mongodb_client.close()

    

app = FastAPI(lifespan=db_lifespan)


allowed_origins = [
    "http://localhost:3000"

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Test route 
@app.get("/")
def read_root():
    return {"Hello": "World"}


# Room routes

@app.get("/rooms", response_model=list[Room])
def read_rooms():
    return  service.get_rooms(app.database)

@app.get("/rooms/devices-summary")
def read_rooms_devices_summary():
    return service.get_rooms_devices_summary(app.database)

@app.get("/rooms/active-devices")
def read_rooms_active_devices():
    return service.get_rooms_active_devices(app.database)


@app.get("/rooms/{room_id}", response_model=Room)
def read_room(room_id: str):
    return service.get_room(room_id=room_id, db=app.database)


@app.post("/rooms", response_model=Room, status_code=201, summary="Create a new room")
def create_room(room: RoomCreate):
    return service.create_room(room, app.database)


@app.patch("/rooms/{room_id}", response_model=Room)
def update_room(room_id: str, room: RoomUpdate):
    return service.update_room(room_id, room, app.database)

@app.get("/rooms/{room_id}/activities", response_model=list[RoomActivity])
def read_room_activities(room_id: str):
    return service.get_room_activities(room_id, app.database)

@app.get("/rooms/{room_id}/consumption")
def read_room_consumption_summary(room_id: str):
    return service.get_room_device_consumption(room_id, app.database)



# Device routes

@app.get("/devices", response_model=list[Device])
def read_devices():
    return service.get_devices(app.database)

@app.get("/devices/consumption-summary")
def read_devices_consumption_summary(
    start_date: Union[datetime, None] = datetime.now() - timedelta(days=7), 
    end_date: Union[datetime, None] = datetime.now()
    ):
    return service.get_devices_consumption_summary(start_date, end_date, app.database)

@app.get("/devices/{device_id}", response_model=Device)
def read_device(device_id: str, include_activities: bool = False, include_room: bool = False, include_consumption: bool = False):
    return service.get_device(device_id=device_id, db=app.database, include_activities=include_activities, include_room=include_room, include_consumption=include_consumption)

@app.get("/devices/{device_id}/activities")
def read_device_activities(device_id: str):
    return service.get_device_activities(device_id, app.database)

@app.get("/devices/{device_id}/consumption")
def read_device_consumption(device_id: str):
    return service.get_device_consumption(device_id, app.database)


@app.post("/devices", response_model=Device, status_code=201, summary="Create a new device")
def create_device(device: DeviceCreate):
    return service.create_device(device, app.database)


@app.patch("/devices/{device_id}", response_model=Device)
def update_device(device_id: str, device: DeviceUpdate):
    return service.update_device(device_id, device, app.database)

# Sensor routes

@app.get("/sensors")
def read_sensors():
    return service.get_sensors(app.database)

@app.get("/sensors/{sensor_id}")
def read_sensor(sensor_id: str):
    return service.get_sensor(sensor_id, app.database)

@app.post("/sensors")
def create_sensor(sensor: SensorCreate):
    return service.create_sensor(sensor, app.database)

@app.patch("/sensors/{sensor_id}")
def update_sensor(sensor_id: str, sensor: SensorUpdate):
    return service.update_sensor(sensor_id, sensor, app.database)


