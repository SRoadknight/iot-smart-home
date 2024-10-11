import pandas as pd 
from datetime import datetime, timedelta
import json 
import random 
import math

# Open zip file
with open('../data/iot_home.zip', 'rb') as f:
    data = pd.read_csv(f, compression='zip', low_memory=False)

# Choose only the columns that are needed
data = data[['time', 'Microwave [kW]', 'Dishwasher [kW]', 'Fridge [kW]', 'temperature']]

# Convert the time to datetime object
data['time'] = pd.to_numeric(data['time'], errors='coerce')
data['time'] = pd.to_datetime(data['time'], unit='s')

# Change time to finish at the current date 
max_time = data['time'].max()
data['time'] = data['time'] - (max_time - datetime.now())

# resample the data to 1 minute intervals
data = data.resample('min', on='time').mean().reset_index()



devices = [
    {"name": "Kitchen-Microwave", "type": "Microwave", "model": "Samsung", "location": "Kitchen", "status": "off", "consumption": []},
    {"name": "Kitchen-Dishwasher","type": "Dishwasher", "model": "LG", "location": "Kitchen", "status": "off", "consumption": []},
    {"name": "Kitchen-Fridge","type": "Fridge", "model": "Whirlpool", "location": "Kitchen", "status": "on", "consumption": []},
]



for _, row in data.iterrows():
    devices[0]['consumption'].append({"timestamp": row['time'].isoformat(), "value": row['Microwave [kW]']})
    devices[1]['consumption'].append({"timestamp": row['time'].isoformat(), "value": row['Dishwasher [kW]']})
    devices[2]['consumption'].append({"timestamp": row['time'].isoformat(), "value": row['Fridge [kW]']})



existing_devices_json = {
    "devices": devices
}

with open('../data/existing_devices.json', 'w') as f:
    json.dump(existing_devices_json, f, indent=4)

sensors = [
    {"name": "Garden-Temp","type": "Temperature", "location": "Garden", "readings": []},
    {"name": "Living-Room-Temp","type": "Temperature", "location": "Living Room", "readings": []}
]



for _, row in data.iterrows():
    sensors[0]['readings'].append({"timestamp": row['time'].isoformat(), "value": math.ceil(row['temperature']*100)/100})
    sensors[1]['readings'].append({"timestamp": row['time'].isoformat(), "value": math.ceil(row['temperature']*100)/100})


existing_sensors_json = {   
    "sensors": sensors
}

with open('../data/existing_sensors.json', 'w') as f:
    json.dump(existing_sensors_json, f, indent=4)



fake_devices = [
    {"name": "Living-Room-Light","type": "Light", "model": "Philips", "location": "Living Room", "status": "off", "count": 4},
    {"name": "Bedroom-Light","type": "Light", "model": "Philips", "location": "Bedroom", "status": "off", "count": 3},
    {"name": "Kitchen-Light","type": "Light", "model": "Philips", "location": "Kitchen", "status": "off", "count": 5},
    {"name": "Bathroom-Light","type": "Light", "model": "Philips", "location": "Bathroom", "status": "off", "count": 1},
    {"name": "Toilet-Light","type": "Light", "model": "Philips", "location": "Toilet", "status": "off", "count": 1},
    {"name": "Balcony-Light","type": "Light", "model": "Philips", "location": "Balcony", "status": "off", "count": 1},
    {"name": "Garage-Light","type": "Light", "model": "Philips", "location": "Garage", "status": "off", "count": 2},
    {"name": "Garage-Door", "type": "Garage Door", "model": "Chamberlain", "location": "Garage", "status": "closed", "count": 1},
    {"name": "Lviing-Smoke", "type": "Smoke Detector", "model": "First Alert", "location": "Living Room", "status": "active", "count": 1},
    {"name": "Bedroom-Smoke", "type": "Smoke Detector", "model": "First Alert", "location": "Bedroom", "status": "active", "count": 1},
    {"name": "Front-Lock", "type": "Door Lock", "model": "Schlage", "location": "Front Door", "status": "closed", "count": 1},
    {"name": "Back-Lock", "type": "Door Lock", "model": "Schlage", "location": "Back Door", "status": "closed", "count": 1},
    {"name": "Living-Blinds", "type": "Smart Blinds", "model": "Somfy", "location": "Living Room", "status": "closed", "count": 1},
    {"name": "Bedroom-Blinds", "type": "Smart Blinds", "model": "Somfy", "location": "Bedroom", "status": "closed", "count": 1}
]

fake_devices_and_activities = []

def add_random_minutes(time, minutes):
    return time + timedelta(minutes=random.randint(-minutes, minutes))

for device in fake_devices:
    if device['type'] == "Light":
        for i in range(device['count']):

            morning_start = data['time'].iloc[0].replace(hour=6, minute=0, second=0)
            morning_end = data['time'].iloc[0].replace(hour=9, minute=0, second=0)
            evening_start = data['time'].iloc[0].replace(hour=18, minute=0, second=0)
            evening_end = data['time'].iloc[0].replace(hour=23, minute=0, second=0)

            morning_start = add_random_minutes(morning_start, 30)
            morning_end = add_random_minutes(morning_end, 30)
            evening_start = add_random_minutes(evening_start, 30)
            evening_end = add_random_minutes(evening_end, 30)

            current_device = {"name": device['name'] + str(i+1), "type": device['type'], "model": device['model'], "location": device['location'], "status": device['status'], "activity": []}
            while morning_start < data['time'].iloc[-1]:
                current_device["activity"].append({"timestamp": morning_start.isoformat(), "activity": "on"})
                current_device["activity"].append({"timestamp": morning_end.isoformat(), "activity": "off"})
                current_device["activity"].append({"timestamp": evening_start.isoformat(), "activity": "on"})
                current_device["activity"].append({"timestamp": evening_end.isoformat(), "activity": "off"})

                morning_start += add_random_minutes(timedelta(days=1), 30)
                morning_end += add_random_minutes(timedelta(days=1), 30)
                evening_start += add_random_minutes(timedelta(days=1), 30)
                evening_end += add_random_minutes(timedelta(days=1), 30)
            fake_devices_and_activities.append(current_device)

    elif device['type'] == "Garage Door":
        for i in range(device['count']):
            morning_leave = data['time'].iloc[0].replace(hour=8, minute=0, second=0)
            evening_return = data['time'].iloc[0].replace(hour=17, minute=30, second=0)

            morning_leave = add_random_minutes(morning_leave, 30)
            evening_return = add_random_minutes(evening_return, 30)

            current_device = {"name": device['name'] + str(i+1),"type": device['type'], "model": device['model'], "location": device['location'], "status": device['status'], "activity": []}
            while morning_leave < data['time'].iloc[-1]:
                current_device["activity"].append({"timestamp": morning_leave.isoformat(), "activity": "open"})
                current_device["activity"].append({"timestamp": evening_return.isoformat(), "activity": "close"})
                morning_leave += add_random_minutes(timedelta(days=1), 30)
                evening_return += add_random_minutes(timedelta(days=1), 30)
            fake_devices_and_activities.append(current_device)
    elif device['type'] == "Smoke Detector":
        for i in range(device['count']):
            alarm_time = data['time'].iloc[0].replace(hour=12, minute=0, second=0)

            alarm_time = add_random_minutes(alarm_time, 600)

            current_device = {"name": device['name'] + str(i+1), "type": device['type'], "model": device['model'], "location": device['location'], "status": device['status'], "activity": []}
            while alarm_time < data['time'].iloc[-1]:
                if random.random() < 0.01:
                    current_device["activity"].append({"timestamp": alarm_time.isoformat(), "activity": "smoke detected"})
                alarm_time += timedelta(days=1)
            fake_devices_and_activities.append(current_device)
    elif device['type'] == "Door Lock":
        for i in range(device['count']):
            morning_leave = data['time'].iloc[0].replace(hour=8, minute=0, second=0)
            evening_return = data['time'].iloc[0].replace(hour=17, minute=30, second=0)

            current_device = {"name": device['name'] + str(i+1),"type": device['type'], "model": device['model'], "location": device['location'], "status": device['status'], "activity": []}
            while morning_leave < data['time'].iloc[-1]:
                current_device["activity"].append({"timestamp": morning_leave.isoformat(), "activity": "lock"})
                current_device["activity"].append({"timestamp": evening_return.isoformat(), "activity": "unlock"})
                morning_leave += add_random_minutes(timedelta(days=1), 30)
                evening_return += add_random_minutes(timedelta(days=1), 30)
            fake_devices_and_activities.append(current_device)
    elif device['type'] == "Automatic Blinds":
        for i in range(device['count']):
            morning_open = data['time'].iloc[0].replace(hour=6, minute=0, second=0)
            evening_close = data['time'].iloc[0].replace(hour=18, minute=0, second=0)

            morning_open = add_random_minutes(morning_open, 30)
            evening_close = add_random_minutes(evening_close, 30)

            current_device = {"name": device['name'] + str(i+1),"type": device['type'], "model": device['model'], "location": device['location'], "status": device['status'], "activity": []}
            while morning_open < data['time'].iloc[-1]:
                current_device["activity"].append({"timestamp": morning_open.isoformat(), "activity": "open"})
                current_device["activity"].append({"timestamp": evening_close.isoformat(), "activity": "close"})
                morning_open += add_random_minutes(timedelta(days=1), 30)
                evening_close += add_random_minutes(timedelta(days=1), 30)
            fake_devices_and_activities.append(current_device)
        

fake_devices_json = {
    "fake_devices_and_activities": fake_devices_and_activities
}

with open('../data/fake_devices.json', 'w') as f:
    json.dump(fake_devices_json, f, indent=4)
