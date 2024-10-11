from datetime import datetime, timedelta
from fastapi import HTTPException
from bson import ObjectId
from typing import Union
from src.utils import PyObjectId, check_valid_room
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
    RoomActivity,
    DeviceActivity,
    RoomConsumption,
    DeviceConsumption
)

# Room functions

def get_rooms(db):
    rooms = db.rooms
    room_list = list(rooms.find({}))

    for room in room_list:
        devices = db.devices
        room['devices'] = list(devices.find({'room_id': room['_id']}))
        sensors = db.sensors
        sensor = sensors.find_one({'room_id': room['_id'], 'type': 'Temperature'})
        if sensor is not None:
            sensor_reading = db.sensor_readings.find_one({'sensor_id': sensor['_id']}, sort=[('timestamp', -1)])

            if sensor_reading is not None:
                room['temperature'] = sensor_reading['value']

    return [Room(**room) for room in room_list]


def get_room(room_id, db):
    oid = ObjectId(room_id)
    
    room = db.rooms.find_one({'_id': oid})

    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    
    devices = db.devices
    room['devices'] = list(devices.find({'room_id': room['_id']}))

    
    return Room(**room)

        
    
    


def create_room(room: RoomCreate, db):
    room_dict = room.model_dump()
    result = db.rooms.insert_one(room_dict)
    room_dict['_id'] = result.inserted_id
    return Room(**room_dict)


def update_room(room_id: str, room: RoomUpdate, db):
    oid = ObjectId(room_id)
    room_dict = room.model_dump(exclude_unset=True)
    result = db.rooms.find_one_and_update({'_id': oid}, {'$set': room_dict}, return_document=True)
    if result is None:
        raise HTTPException(status_code=404, detail="Room not found")
    
    return Room(**result)

def get_room_activities(room_id, db, limit: int = 25):
    oid = ObjectId(room_id)
    pipeline = [

           {
            '$match': {
                '_id': oid
            }
        },
        {
            '$lookup': {
                'from': 'devices',
                'localField': '_id',
                'foreignField': 'room_id',
                'as': 'devices'
            }
        },
        {
            '$unwind': '$devices'
        },
        {
            '$lookup': {
                'from': 'device_activity',
                'localField': 'devices._id',
                'foreignField': 'device_id',
                'as': 'activities'
            }
        },
        {
            '$unwind': '$activities'
        },
     
        {
            '$project': {
                'activity_id': '$activities._id',
                'device_type': '$devices.type',
                'device_model': '$devices.model',
                'timestamp': '$activities.timestamp',
                'activity': '$activities.activity',
                'device_id': '$devices._id',
                'device_name': '$devices.name'
            }
        },
        {
            '$sort': {
                'timestamp': -1
            }
        },
        {
            '$limit': limit
        }
    ]


    activities = db.rooms.aggregate(pipeline)
    return [RoomActivity(
        activity_id=activity['activity_id'],
        device_type=activity['device_type'],
        device_model=activity['device_model'],
        timestamp=activity['timestamp'],
        activity=activity['activity'],
        device_id=activity['device_id'],
        device_name=activity['device_name']
    ) for activity in activities]


def get_room_device_consumption(room_id, db, limit: int = 25):
    oid = ObjectId(room_id)
    pipeline = [
        {
            '$match': {
                '_id': oid
            }
        },
        {
            '$lookup': {
                'from': 'devices',
                'localField': '_id',
                'foreignField': 'room_id',
                'as': 'devices'
            }
        },
        {
            '$unwind': '$devices'
        },
        {
            '$lookup': {
                'from': 'device_consumption',
                'localField': 'devices._id',
                'foreignField': 'device_id',
                'as': 'consumption'
            }
        },
        {
            '$unwind': '$consumption'
        },
        {
            '$project': {
                'device_id': '$devices._id',\
                'consumption_id': '$consumption._id',
                'device_name': '$devices.name',
                'device_type': '$devices.type',
                'device_model': '$devices.model',
                'device_consumption': '$consumption.value',
                'timestamp': '$consumption.timestamp'
            }
        },
        {
            '$sort': {
                'timestamp': -1
            }
        },
        {
            '$limit': limit
        }
    ]

    devices = db.rooms.aggregate(pipeline)
    return [RoomConsumption(
        device_id=device['device_id'],
        consumption_id=device['consumption_id'],
        device_name=device['device_name'],
        device_type=device['device_type'],
        device_model=device['device_model'],
        device_consumption=device['device_consumption'],
        timestamp=device['timestamp']
    ) for device in devices]




# Device functions

def get_devices(db):
    
    pipeline = [
        {
            '$lookup': {
                'from': 'rooms',
                'localField': 'room_id',
                'foreignField': '_id',
                'as': 'room'
            }
        },
        {
            '$unwind': '$room'
        }
    ]
    devices = db.devices.aggregate(pipeline)
    return [Device(**device) for device in devices]

def get_device(*,
                device_id: str, 
                db, 
                include_activities: bool = False, 
                include_room: bool = False, 
                include_consumption: bool = False,
                start_date: datetime = datetime.now() - timedelta(days=7),
                end_date: datetime = datetime.now()):
    oid = ObjectId(device_id)
    device = db.devices.find_one({'_id': oid})
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    
    device = Device(**device)

    if include_activities:
        activities = get_device_activities(device_id, db)
        device.activities = activities

    if include_consumption:
        consumption = get_device_consumption(device_id, db, start_date, end_date)
        device.consumption = consumption


    room_oid = ObjectId(device.room_id)
    room = db.rooms.find_one({'_id': room_oid})
    if room is not None:
        device.room = Room(**room)


    return device


def create_device(device: DeviceCreate, db):
    device_dict = device.model_dump()
    device_dict['room_id'] = check_valid_room(device_dict['room_id'], db)
    result = db.devices.insert_one(device_dict)
    device_dict['_id'] = result.inserted_id
    return Device(**device_dict)

def update_device(device_id: str, device: DeviceUpdate, db):
    oid = ObjectId(device_id)
    if device.room_id is not None:
        device.room_id = check_valid_room(device.room_id, db)
    device_dict = device.model_dump(exclude_unset=True)
    result = db.devices.find_one_and_update({'_id': oid}, {'$set': device_dict}, return_document=True)

    if result is None:
        raise HTTPException(status_code=404, detail="Device not found")
    
    return Device(**result)

def get_devices_consumption_summary(start_date, end_date, db):
    pipeline = [
        {
            "$lookup": {
                "from": "device_consumption",
                "localField": "_id",
                "foreignField": "device_id",
                "as": "consumption"
            }
        },
        {"$unwind": "$consumption"},
        {
            "$match": {
                "consumption.timestamp": {
                    "$gte": start_date,
                    "$lte": end_date
                }
            }
        },
        {
            "$group": {
                "_id": "$_id",
                "device": {"$first": "$$ROOT"},
                "total_consumption": {"$sum": "$consumption.value"}
            }
        },
        {
            "$project": {
                "device": 1,
                "total_consumption": 1
            }
        },
        {
            "$sort": {
                "total_consumption": -1
            }
        }
    ]
    devices = db.devices.aggregate(pipeline)
    return [Device(**device['device']) for device in devices]


def get_device_activities(device_id, db):
    oid = ObjectId(device_id)
    device = db.devices.find_one({'_id': oid})
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    

    activities = db.device_activity.find({'device_id': oid})

    return [DeviceActivity(**activity) for activity in activities]


def get_device_consumption(
        device_id, 
        db, start_date: Union[datetime, None] = datetime.now() - timedelta(days=7),
        end_date: Union[datetime, None]  = datetime.now(),
        limit: int = 25):
    oid = ObjectId(device_id)
    pipeline = [
        {
            '$match': {
                'device_id': oid,
                'timestamp': {
                    '$gte': start_date,
                    '$lte': end_date
                }
            }
        },
        {
            '$sort': {
                'timestamp': -1
            }
        },
        {
            '$limit': limit
        }
    ]
    consumption = db.device_consumption.aggregate(pipeline)
    return [DeviceConsumption(**consumption) for consumption in consumption] 


# Sensor functions

def get_sensors(db):
    sensors = db.sensors
    sensor_list = list(sensors.find())
    return [Sensor(**sensor) for sensor in sensor_list]

def get_sensor(sensor_id: str, db):
    oid = ObjectId(sensor_id)
    sensor = db.sensors.find_one({'_id': oid})
    if sensor is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    
    return Sensor(**sensor)

def create_sensor(sensor: SensorCreate, db):
    sensor_dict = sensor.model_dump()
    sensor_dict['room_id'] = check_valid_room(sensor_dict['room_id'], db)
    result = db.sensors.insert_one(sensor_dict)
    sensor_dict['_id'] = result.inserted_id
    return Sensor(**sensor_dict)

def update_sensor(sensor_id: str, sensor: SensorUpdate, db):
    oid = ObjectId(sensor_id)
    if sensor.room_id is not None:
        sensor.room_id = check_valid_room(sensor.room_id, db)
    sensor_dict = sensor.model_dump(exclude_unset=True)
    result = db.sensors.find_one_and_update({'_id': oid}, {'$set': sensor_dict}, return_document=True)

    if result is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    
    return Sensor(**result)

def get_rooms_devices_summary(db):
    pipeline = [
        {
            '$lookup': {
                'from': 'devices',
                'localField': '_id',
                'foreignField': 'room_id',
                'as': 'devices'
            }
        }
    ]
    rooms = db.rooms.aggregate(pipeline)
    [Room(**room) for room in rooms]


def get_rooms_active_devices(db):
    pipeline = [
        {
            '$lookup': {
                'from': 'devices',
                'localField': '_id',
                'foreignField': 'room_id',
                'as': 'devices'
            }
        },
        {
            '$unwind': '$devices'
        },
        {
            '$match': {
                'devices.status': 'on'
            }
        },
        {
            '$group': {
                '_id': '$_id',
                'name': {'$first': '$name'},
                'devices': {'$push': '$devices'}
            }
        }
    ]
    rooms = db.rooms.aggregate(pipeline)
    return [Room(**room) for room in rooms]



