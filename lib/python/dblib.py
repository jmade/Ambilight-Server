
import pymysql.cursors
import time

DB_PASS = 'tabard5]deathblows'
DB_USER = 'app'
DB_NAME = 'ambi'


def makeConnection(db_name=DB_NAME):
	return pymysql.connect(
		host='localhost',
		user=DB_USER,
		password=DB_PASS,
		db=db_name,
		charset='utf8mb4',
		cursorclass=pymysql.cursors.DictCursor
		)


def call_sp(sql):
	connection = makeConnection()
	try:
		with connection.cursor() as cursor:
			cursor.execute(str(sql))
			result = cursor.fetchall()
		connection.commit()
	finally:
		connection.close()
	if result is None:
		result = 0
	return result
	

def sensorDB(sql):
	connection = makeConnection(db_name='Sensor')
	try:
		with connection.cursor() as cursor:
			cursor.execute(sql)
			result = cursor.fetchall()
		connection.commit()
	finally:
		connection.close()
	if result is None:
		result = 0
	return result


def call_sql(raw_sql:str):
	connection = makeConnection()
	try:
		with connection.cursor() as cursor:
			cursor.execute(raw_sql)
			result = cursor.fetchall()
		connection.commit()
	finally:
		connection.close()
	if result is None:
		result = 0
	return result


# type stuff
def now():
	return time.strftime('%Y-%m-%d %H:%M:%S')

def DateFromTicks(ticks):
	return Date(*time.localtime(ticks)[:3])

def TimeFromTicks(ticks):
	return Time(*time.localtime(ticks)[3:6])

def TimestampFromTicks(ticks):
	return Timestamp(*time.localtime(ticks)[:6])


def json_defaults(obj):
	if isinstance(obj, datetime.datetime):
		return str(obj)
	if isinstance(obj, decimal.Decimal):
		return float(obj)
	if isinstance(obj, long):
		return str(obj)
	raise TypeError