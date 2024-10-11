from pymongo import MongoClient
import datetime
import json 
import os 

# Connect to the database
connection_string = os.environ['MONGO_CONNECTION_STRING']

client = MongoClient(connection_string)

# Drop database and associated users
if 'iot_home' in client.list_database_names():
    client.drop_database('iot_home')
    print("Database dropped")

admin_db = client.admin



# Create user for web app
try:
    admin_db.command("createUser", "iot_home_web", pwd="iot_home_web", roles=[{"role": "readWrite", "db": "iot_home"}])
    print("Web app user created")
except Exception as e:
    print("Failed to create web app user", str(e))

# Create user for data analyst
try:
    admin_db.command("createUser", "iot_home_analyst", pwd="iot_home_analyst", roles=[{"role": "read", "db": "iot_home"}])
    print("Data analyst user created")
except Exception as e:
    print("Failed to create data analyst user", str(e))

db = client.iot_home

# Room collection
rooms = db.rooms
# Insert rooms
room_list = [
    {"name": "Living Room"},
    {"name": "Bedroom"},
    {"name": "Kitchen"},
    {"name": "Bathroom"},
    {"name": "Toilet"},
    {"name": "Balcony"},
    {"name": "Garage"},
    {"name": "Front Door"},
    {"name": "Back Door"},
    {"name": "Garden"}
]
rooms.insert_many(room_list)

room_ids = {room['name']: room['_id'] for room in rooms.find()}

# Device collection
devices = db.devices
devices.create_index('room_id')

# Sensor collection
sensors = db.sensors
sensors.create_index('room_id')

# Device consumption collection
device_consumption = db.create_collection('device_consumption', capped=True, size=65000000, max=650000)
device_consumption.create_index([('device_id', 1), ('timestamp', 1)])

# Device activity collection
device_activity = db.create_collection('device_activity', capped=True, size=300000, max=3000)
device_activity.create_index([('device_id', 1), ('timestamp', 1)])

# Sensor data collection
sensor_readings = db.create_collection('sensor_readings', capped=True, size=22000000, max=22000)
sensor_readings.create_index([('sensor_id', 1), ('timestamp', 1)])



def insert_existing_devices_and_consumption():
    # Load the existing devices and consumption
    with open('../data/existing_devices.json') as f:
        data = json.load(f)

    # Insert existing devices
    for device in data['devices']:
        device_setup = {
            "name": device['name'],
            "type": device['type'],
            "model": device['model'],
            "room_id": room_ids[device['location']],
            "status": device['status']
        }
        device_id = devices.insert_one(device_setup).inserted_id

        device_consumption_batch = []
        # Insert device consumption
        for consumption in device['consumption']:
            consumption_setup = {
                "device_id": device_id,
                "timestamp": datetime.datetime.fromisoformat(consumption['timestamp']),
                "value": consumption['value']
            }
            device_consumption_batch.append(consumption_setup)
        device_consumption.insert_many(device_consumption_batch)

def insert_existing_sensors_and_readings():
    # Load the existing sensors and readings
    with open('../data/existing_sensors.json') as f:
        data = json.load(f)

    # Insert existing sensors
    for sensor in data['sensors']:
        sensor_setup = {
            "name": sensor['name'],
            "type": sensor['type'],
            "room_id": room_ids[sensor['location']]
        }
        sensor_id = sensors.insert_one(sensor_setup).inserted_id

        readings_batch = []
        # Insert sensor readings
        for reading in sensor['readings']:
            reading_setup = {
                "sensor_id": sensor_id,
                "timestamp": datetime.datetime.fromisoformat(reading['timestamp']),
                "value": reading['value']
            }
            readings_batch.append(reading_setup)
        sensor_readings.insert_many(readings_batch)


def insert_fake_devices_and_activities():
    # Load the fake devices and activities
    with open('../data/fake_devices.json') as f:
        data = json.load(f)

    # Insert fake devices

    for device in data['fake_devices_and_activities']:
        device_setup = {
            "name": device['name'],
            "type": device['type'],
            "model": device['model'],
            "room_id": room_ids[device['location']],
            "status": device['status']
        }
        device_id = devices.insert_one(device_setup).inserted_id

        # Insert device activity
        for activity in device['activity']:
            activity_setup = {
                "device_id": device_id,
                "timestamp": datetime.datetime.fromisoformat(activity['timestamp']),
                "activity": activity['activity']
            }
            device_activity.insert_one(activity_setup)


if __name__ == "__main__":
    insert_existing_devices_and_consumption()
    insert_existing_sensors_and_readings()
    insert_fake_devices_and_activities()
    print("Database initialised")

