
import requests
from requests.exceptions import Timeout

from lib.python.dblib import sensorDB


from enum import Enum

class classproperty(object):
    def __init__(self, getter):
        self.getter= getter
    def __get__(self, instance, owner):
        return self.getter(owner)

class SensorType(Enum):
    DS18B20 = 'DS18B20'
    AM2301 = 'AM2301'
    DHT22 = 'DHT22'
    DHT11 = 'DHT11'

    @classproperty
    def __values__(cls):
        return [m.value for m in cls]


DEVICES = [
	# SensorServer
	# { 'title' : 'SensorServer', 'room_id': 4, 'sensor_id' : [{'T':3},{'H':2}],   'address' : "19", 'sensor' : SensorType.DHT11   },
	# Sonoff Devices
	# { 'title' : 'Test',         'room_id': 0, 'sensor_id' : [{'T':8}],           'address' : "34", 'sensor' : SensorType.DS18B20 },
	# { 'title' : 'Bench Sonoff', 'room_id': 0, 'sensor_id' : [{'T':9},{'H':10}],  'address' : "33", 'sensor' : SensorType.DHT22   },
	# { 'title' : 'Spare Sonoff', 'room_id': 0, 'sensor_id' : [{'T':13},{'H':14}], 'address' : "36", 'sensor' : SensorType.DHT11   },

	{ 'title' : 'Outside',      'room_id': 0, 'sensor_id' : [{'T':4},{'H':5}],   'address' : "32", 'sensor' : SensorType.DHT22   },
	{ 'title' : 'Bedroom',      'room_id': 0, 'sensor_id' : [{'T':6},{'H':7}],   'address' : "31", 'sensor' : SensorType.DHT11   },
	{ 'title' : 'Kitchen Sink', 'room_id': 0, 'sensor_id' : [{'T':11},{'H':12}], 'address' : "37", 'sensor' : SensorType.DHT11   },
	
]

ROOM_ID_LOOKUP = {
	'bedroom' : 2,
	'outside' : 3,
	'backyard' : 3,
	'office' : 4,
	'kitchen' : 5,
}


ROOM_SENSOR_ID_LOOKUP = {
	'bedroom' : [{'temperature':6},{'humidity':7}],
	'outside' : [{'temperature':4},{'humidity':5}],
	'backyard': [{'temperature':4},{'humidity':5}],
	'office'  : [{'temperature':13},{'humidity':14},{'temperature':9},{'humidity':10}],
	'kitchen' : [{'temperature':11},{'humidity':12}],
}

 
LAST_READING_FOR_ROOM = {
	'bedroom' : None,
	'outside' : None,
	'backyard': None,
	'office'  : None,
	'kitchen' : None,
}




TEMP_CHAR_ID = 1
HUM_CHAR_ID = 3


# def express_reading_for(room_name, convertTemp=False):
# 	global LAST_READING_FOR_ROOM

# 	if room_name in LAST_READING_FOR_ROOM:
# 		last_reading = LAST_READING_FOR_ROOM[room_name]
# 		if last_reading is not None:
# 			print("Reading From Cache!:",last_reading)
# 			return last_reading
# 		else:
# 			print("LAST_READING_FOR_ROOM Value was 'None' for {}\nGetting Express Readings...".format(room_name))
# 			resp = get_express_readings_for(room_name, convertTemp=False)
# 			if resp is not None:
# 			else:
# 				print("ERROR getting 'get_express_readings_for' Room Name:{}".format(room_name))
# 				return False
# 	else:
# 		print("ERROR - Room Name Not Found ({})".format(room_name))
# 		return False


def get_express_readings_for(room_name, convertTemp=False):
	response = None
	if room_name in ROOM_SENSOR_ID_LOOKUP:
		response = {}
		sensor_id_bundle = ROOM_SENSOR_ID_LOOKUP[room_name]
		if len(sensor_id_bundle) > 2:
			# do averages too
			t = []
			h = []
			for entry in sensor_id_bundle:
				title = next(iter(entry))
				sensor_id = entry[title]
				sql = "select reading from LastSensorReading where sensorId={}".format(sensor_id)
				reading = sensorDB(sql)[0]['reading']
				if title == 'temperature':
					if convertTemp:
						reading = (float(reading) - 32.0) * 5.0/9.0
					t.append(reading)
				if title == 'humidity':
					h.append(reading)
			t_val = sum(t) / len(t) if len(t) > 1 else t[0]
			h_val = sum(h) / len(h) if len(h) > 1 else h[0]
			response['temperature'] = float("{:.2f}".format(t_val))
			response['humidity'] = int(h_val)
		else:
			for entry in sensor_id_bundle:
				title = next(iter(entry))
				sensor_id = entry[title]
				sql = "select reading from LastSensorReading where sensorId={}".format(sensor_id)
				reading = sensorDB(sql)[0]['reading']

				if title == 'temperature':
					if convertTemp:
						reading = (float(reading) - 32.0) * 5.0/9.0
					reading = float("{:.2f}".format(reading))
				if title == 'humidity':
					reading = int(reading)
				response[title] = reading

	return response




# Sensor Helpers
def get_sensor_ids(title):
	for device in DEVICES:
		if device['title'] == title:
			return device['sensor_id']

def get_sensor_id(id_list,key):
	for item in id_list:
		for k,v in item.items():
			if k == key:
				return v

def get_last_reading(sensor_id):
	sql =  'select reading from SensorReadings '
	sql += 'where sensorId={} '.format(sensor_id)
	sql += 'order by created desc limit 1'
	sql += ';'
	last_readings = sensorDB(sql)
	return last_readings

def get_sensors_for(room):
	room_id = ROOM_ID_LOOKUP.get(room,None)
	if room_id is None:
		return []
	sql = 'select * from Sensor where room_id={};'.format(room_id)
	sensors = sensorDB(sql)
	return sensors

def fix_readings(r,convertTemp=False):

	if len(r) < 1:
		if convertTemp:
			return { 'temperature' : 32.0, 'humidity' : 0 }
		else:
			return { 'temperature' :0, 'humidity' : 0 }

	t = None
	h = None

	if 'temperature' in r:
		t = r['temperature']
	if 'Temperature' in r:
		t = r['Temperature']

	if 'humidity' in r:
		h = r['humidity']
	if 'Humidity' in r:
		h = r['Humidity']

	if t is None or h is None:
		if convertTemp:
			return { 'temperature' : 32.0, 'humidity' : 0 }
		else:
			return { 'temperature' : 0 , 'humidity' : 0 }

	if t == 0.0:
		if convertTemp:
			t = 32.0

	if convertTemp:
		t = (float(t) - 32.0) * 5.0/9.0
	t = float("{:.2f}".format(t))

	return {
		'temperature' : float(t),
		'humidity' : int(float(h)),
	}

def average_readings(readings):

	if len(readings) < 1:
		return { 'temperature' : 0.0, 'humidity' : 0 }
	
	temp_readings = []
	humidity_readings = []

	for r in readings:
		if 'temperature' in r:
			temp_readings.append(r['temperature'])
		if 'humidity' in r:
			humidity_readings.append(r['humidity'])

	humidity = 0
	temperature = 0.0
	total_temp = 0.0
	total_humidity = 0.0

	for t in temp_readings:
		total_temp += t
	for h in humidity_readings:
		total_humidity += h

	if total_temp != 0.0:
		if len(temp_readings):
			temperature = total_temp / float(len(temp_readings))

	temperature = float("{:.2f}".format(temperature))
	if len(humidity_readings):
		humidity = total_humidity / float(len(humidity_readings))

	return {
		'temperature' : float(temperature),
		'humidity' : int(float(humidity)),
	}


def get_sensor_readings_for_room(room):
	readings = {}
	room_sensors = get_sensors_for(room)
	all_readings = []
	for s in room_sensors:
		if 'id' in s and 'characteristic_id' in s:
			sensorId = s['id']
			last_reading = get_last_reading(sensorId)
			charId = s['characteristic_id']
			if charId == TEMP_CHAR_ID:
				readings['temperature'] = last_reading[0]['reading']
			if charId == HUM_CHAR_ID:
				readings['humidity'] = last_reading[0]['reading']
			if 'temperature' in readings and 'humidity' in readings:
				all_readings.append(readings)
	avg_readings = average_readings(all_readings)
	formated_readings = fix_readings(avg_readings,True)
	return formated_readings


def multi_sensor_insert(insertion_str):
	sql = 'insert into SensorReadings (`sensorId`,`reading`) values '
	sql += insertion_str
	sql += ';'
	result = sensorDB(sql)
	return True

def multi_sensor_last_update(readings):
	sql = ''
	for sensorId,reading in readings:
		sql = "update LastSensorReading set reading={} where id={};".format(reading,sensorId)
		result = sensorDB(sql)
	return True

def run_sensor_task():
	insert = ''
	reading_tup = []
	readings = gather_sensor_readings()
	for reading in readings:
		title = next(iter(reading))
		sensor_ids = get_sensor_ids(title)
		value = reading[title]
		if 'temperature' in value:
			temperature_reading = value['temperature']
			sensorId = get_sensor_id(sensor_ids,'T')
			if sensorId is not None:
				insert += '({}, {}),'.format(sensorId,temperature_reading)
				reading_tup.append((sensorId,temperature_reading))
		if 'humidity' in value:
			humidity_reading = value['humidity']
			sensorId = get_sensor_id(sensor_ids,'H')
			if sensorId is not None:
				insert += '({}, {}),'.format(sensorId,humidity_reading)
				reading_tup.append((sensorId,humidity_reading))
	multi_sensor_insert(insert[0:-1])
	multi_sensor_last_update(reading_tup)
	return True

# HTML Parsing
def extract_readings(readings,sensorType,convertTemp=False):
	temperature = None
	humidity = None

	if sensorType == SensorType.DHT11 or sensorType == SensorType.DHT22 or sensorType == SensorType.AM2301:
		chopped = readings.split('m}')
		temperature = chopped[1].split('&')[0]
		if len(chopped) > 2:
			humidity = chopped[2].split('.')[0]
	elif sensorType == SensorType.DS18B20:
		chopped = readings.split('m}')
		temperature = chopped[1].split('&')[0]
	else:
		print('Not Found')

	values = {}
	if temperature is not None:
		if convertTemp:
			temperature = (float(temperature) - 32.0) * 5.0/9.0
		values['temperature'] = float(temperature)
	if humidity is not None:
		values['humidity'] = int(float(humidity))
	values['sensor'] = sensorType.value
	return values


def read_temp_from_SensorServer():
	reading = { 'sensor' : SensorType.DHT11.value }
	# Temp
	try:
		response = requests.get('http://192.168.0.19/temperature', timeout=(10, 10))
	except Timeout:
		print('The request to SensorServer timed out')
	else:
		temperature = response.content.decode('utf-8')
		if temperature != "--":
			reading['temperature'] = float(temperature)
	# Humidity
	try:
		response = requests.get('http://192.168.0.19/humidity', timeout=(10, 10))
	except Timeout:
		print('The request to SensorServer timed out')
	else:
		humidity = response.content.decode('utf-8')
		if humidity != '--':
			reading['humidity'] = int(float(humidity))

	return reading


def get_device_with_name(name):
	parsed_devices = [ device for device in DEVICES if device['title'] == name ]
	if len(parsed_devices):
		return parsed_devices[0]


def get_outside_readings(convertTemp=False):
	device = get_device_with_name('Outside')
	if device is not None:
		return get_readings_from_device(device,convertTemp)


def get_bedroom_readings(convertTemp=False):
	device = get_device_with_name('Bedroom')
	if device is not None:
		return get_readings_from_device(device,convertTemp)


def get_readings_from_device(device,convertTemp=False):
	sensorType = device['sensor']
	address = device['address']
	if address == '19':
		ss_resp = read_temp_from_SensorServer()
		if convertTemp:
			ss_resp['temperature'] = (float(ss_resp['temperature']) - 32.0) * 5.0/9.0
		ss_resp['temperature'] = float("{:.2f}".format(ss_resp['temperature']))
		return  {
				'temperature' : float(ss_resp['temperature']),
				'humidity' : int(float(ss_resp['humidity']))
			}
	else:
		try:
			response = requests.get('http://192.168.0.{}/?m=0'.format(address), timeout=(10, 10))	
		except Timeout:
			print('The request timed out')
			return { 'temperature' : 0.0, 'humidity' : 0 }
		else:
			page = response.content.decode('utf-8')
			readings = extract_readings(page,sensorType)
			if convertTemp:
				readings['temperature'] = (float(readings['temperature']) - 32.0) * 5.0/9.0
			readings['temperature'] = float("{:.2f}".format(readings['temperature']))
			return {
				'temperature' : float(readings['temperature']),
				'humidity' : int(float(readings['humidity']))
			}


def gather_sensor_readings():
	results = []
	for device in DEVICES:
		sensorType = device['sensor']
		address = device['address']
		if address == '19':
			results.append({ device['title'] : read_temp_from_SensorServer() })
		else:
			try:
				response = requests.get('http://192.168.0.{}/?m=0'.format(address), timeout=(10, 10))	
			except Timeout:
				print('The request timed out')
			else:
				page = response.content.decode('utf-8')
				results.append({ device['title'] : extract_readings(page,sensorType) })
	return results



def average_all_devices(convertTemp=False):
	temp_readings = []
	humidity_readings = []
	for reading in gather_sensor_readings():
		title = next(iter(reading))
		readings = reading[title]
		if 'temperature' in readings:
			temp_readings.append(readings['temperature'])
		if 'humidity' in readings:
			humidity_readings.append(readings['humidity'])

	total_temp = 0.0
	for t in temp_readings:
		total_temp += t

	total_humidity = 0.0
	for h in humidity_readings:
		total_humidity += h

	temperature = 0.0
	if total_temp != 0.0:
		if len(temp_readings):
			temperature = total_temp / float(len(temp_readings))
	if convertTemp:
		temperature = (float(temperature) - 32.0) * 5.0/9.0


	temperature = float("{:.2f}".format(temperature))
	if len(humidity_readings):
		humidity = total_humidity / float(len(humidity_readings))

	return {
		'temperature' : float(temperature),
		'humidity' : int(float(humidity)),
	}


def read_sensors(room,convertTemp=False):
	loweredRoom = room.lower()
	express_readings = get_express_readings_for(loweredRoom,convertTemp)
	if express_readings is not None:
		print("Got Express!: ",express_readings)
		return express_readings  
	else:
		print("Express was None; falling back.")
		return get_sensor_readings_for_room(loweredRoom)


def sensor_task():
	# run_sensor_task()
	return "Task Complete" #{ 'message' : "Task Complete" }

