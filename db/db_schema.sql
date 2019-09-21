-- Room
CREATE TABLE Room (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(32) NOT NULL);
-- insert into Room (`name`) values ('Default');


-- Sensors

-- Sensor Type 
CREATE TABLE SensorType (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
type VARCHAR(32) NOT NULL,
created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Type
-- Temperature  
-- insert into SensorType (`type`) values ('Temperature');

-- Humidity  
-- insert into SensorType (`type`) values ('Humidity');


CREATE TABLE SensorCharacteristic (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
sensorType_id INT,
name VARCHAR(32) NOT NULL,
precise BOOLEAN DEFAULT FALSE,
unitMeasurement VARCHAR(32) DEFAULT NULL,
valuePre VARCHAR(32) DEFAULT NULL,
valuePost VARCHAR(32) DEFAULT NULL
);

-- Temperature (Fahrenheit)
-- insert into SensorCharacteristic (`sensorType_id`,`name`,`precise`,`unitMeasurement`,`valuePre`,`valuePost`) values (1, 'Temperature (Fahrenheit)',1,'Degrees Fahrenheit','NULL','°F');

-- Temperature (Celcius)
-- insert into SensorCharacteristic (`sensorType_id`,`name`,`precise`,`unitMeasurement`,`valuePre`,`valuePost`) values (1, 'Temperature (Celcius)',1,'Degrees Celcius','NULL','°C');

-- Relative Humidity
-- insert into SensorCharacteristic (`sensorType_id`,`name`,`precise`,`unitMeasurement`,`valuePost`) values (2, 'Humidity',0,'Relative Humidity','%');


CREATE TABLE Sensor (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
characteristic_id INT NOT NULL,
name VARCHAR(32) NOT NULL,
modelName VARCHAR(32) DEFAULT NULL,
url VARCHAR(32) DEFAULT NULL,
room_id INT DEFAULT NULL,
created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP);

-- insert into Sensor (`characteristic_id`,`name`,`modelName`) values (2, 'DefaultRoom Humidity','DHT-11');

insert into Sensor (`characteristic_id`,`name`,`modelName`) values (2, 'Office Humidity','DHT-22'); -- Office Humidity Sensor id = 1
insert into Sensor (`characteristic_id`,`name`,`modelName`) values (2, 'Office Temperature','DHT-22'); -- Office Temperature Sensor id = 2

-- characteristic_id (Temp(F),1) (Humidity,3)

-- Outside (room_id=3) DHT-22
-- Temp
insert into Sensor (`characteristic_id`,`name`,`modelName`,`url`,`room_id`) values (1, 'Temperature','DHT-22','http://192.168.0.32',3); 

-- Humidity
insert into Sensor (`characteristic_id`,`name`,`modelName`,`url`,`room_id`) values (3, 'Humidity','DHT-22','http://192.168.0.32',3); 


-- BedRoom (room_id=2) DHT-11
-- Temp
insert into Sensor (`characteristic_id`,`name`,`modelName`,`url`,`room_id`) values (1, 'Temperature','DHT-11','http://192.168.0.31',2); 

-- Humidity
insert into Sensor (`characteristic_id`,`name`,`modelName`,`url`,`room_id`) values (3, 'Humidity','DHT-11','http://192.168.0.31',2); 

-- Office 
insert into Sensor (`characteristic_id`,`name`,`modelName`,`url`,`room_id`) values (1, 'Sonoff Temperature','DS18B20','http://192.168.0.34',4);


insert into Sensor (`characteristic_id`,`name`,`modelName`,`url`,`room_id`) values (1, 'Bench Sonoff Temperature','DHT-22','http://192.168.0.33',4); 

-- Humidity
insert into Sensor (`characteristic_id`,`name`,`modelName`,`url`,`room_id`) values (3, 'Bench Sonoff Humidity','DHT-22','http://192.168.0.33',4); 


-- Kitchen (RoomId=5)
-- Temp
insert into Sensor (`characteristic_id`,`name`,`modelName`,`url`,`room_id`) values (1, 'Kitchen Sink Temperature','DHT-11','http://192.168.0.37',5); 
-- Humidity
insert into Sensor (`characteristic_id`,`name`,`modelName`,`url`,`room_id`) values (3, 'Kitchen Sink Humidity','DHT-11','http://192.168.0.37',5);

-- Office (RoomId=4)
-- Temp
insert into Sensor (`characteristic_id`,`name`,`modelName`,`url`,`room_id`) values (1, 'Sonoff Spare Temperature','DHT-11','http://192.168.0.36',4); 
-- Humidity
insert into Sensor (`characteristic_id`,`name`,`modelName`,`url`,`room_id`) values (3, 'Sonoff Spare Humidity','DHT-11','http://192.168.0.36',4);





CREATE TABLE SensorReadings (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
sensorId INT,
reading DOUBLE DEFAULT NULL,
readingTimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- insert into SensorReadings (`sensorId`,`reading`) values (2, 0.123);

CREATE TABLE LastSensorReading (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
sensorId INT,
reading DOUBLE DEFAULT NULL,
readingTimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


insert into LastSensorReading (`sensorId`,`reading`) values (1, 100.123),(2, 100.123),(3, 100.123),(4, 100.123),(5, 100.123),(6, 100.123),(7, 100.123),(8, 100.123),(9, 100.123),(10, 100.123),(11, 100.123),(12, 100.123),(13, 100.123),(14, 100.123);



-- Sensor Assignment Table HaHa
CREATE TABLE SensorAssignment (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
sensorId INT NOT NULL,
roomId INT NOT NULL,
dateAssigned TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
dateRemoved TIMESTAMP DEFAULT '0000-00-00 00:00:00'
);

-- insert into SensorAssignment (`sensorId`,`roomId`) values (1, 1);
-- update SensorAssignment set `dateRemoved` = CURRENT_TIMESTAMP where id=1;









# Location
CREATE TABLE location (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
sessionId INT NOT NULL,
latitude DOUBLE,
longitude DOUBLE,
speed DOUBLE,
locationTimestamp TIMESTAMP,
horizontalAccuracy DOUBLE,
verticalaccuracy DOUBLE,
coarse DOUBLE,
timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

# Heading
CREATE TABLE heading (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, 
headingTrue DOUBLE,
magnetic DOUBLE,
headingTimestamp TIMESTAMP,
accuracy DOUBLE,
x DOUBLE,
y DOUBLE, 
z DOUBLE,
coarse DOUBLE,
sessionId INT NOT NULL,
timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

# Track
CREATE TABLE track (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
sessionId INT NOT NULL,
latitude DOUBLE,
longitude DOUBLE,
speed DOUBLE,
direction CHAR(2),
headingLocalTime VARCHAR(24),
locationLocalTime VARCHAR(24),
locationTimestamp TIMESTAMP,
locationHorizontalAccuracy DOUBLE,
locationVerticalAccuracy DOUBLE,
locationCoarse DOUBLE,
headingTrue DOUBLE,
headingMagnetic DOUBLE,
headingTimestamp TIMESTAMP,
headingAccuracy DOUBLE,
headingX DOUBLE,
headingY DOUBLE, 
headingZ DOUBLE,
headingCoarse DOUBLE,
timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP);





# Session
CREATE TABLE session (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
trackId INT,
updateInterval DOUBLE,
end TIMESTAMP NOT NULL DEFAULT '1970-01-01 00:00:01',
start TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

/*
New Session table with:

entryCount INT,
isActive BOOL,

*/

#Ammendment statement.
ALTER TABLE session ADD COLUMN entryCount INT;
ALTER TABLE session ADD COLUMN isActive BOOL;

#Update to set default values.
UPDATE session SET entryCount = '0' WHERE entryCount IS NULL;
UPDATE session SET isActive = '0' WHERE isActive IS NULL;

-- ALTER TABLE table_name ALTER COLUMN column_name SET DEFAULT 'literal';

ALTER TABLE session MODIFY COLUMN entryCount INT DEFAULT '0';
ALTER TABLE session MODIFY COLUMN isActive BOOL DEFAULT '1';

# New Session Create Statement
CREATE TABLE session (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
trackId INT,
updateInterval DOUBLE,
entryCount INT,
isActive BOOL,
end TIMESTAMP NOT NULL DEFAULT '1970-01-01 00:00:01',
start TIMESTAMP DEFAULT CURRENT_TIMESTAMP);





# Start Session
INSERT INTO session (`id`,`trackId`,`updateInterval`, `start`, `end`) VALUES (0,1,2.5,CURRENT_TIMESTAMP,'1970-01-01 00:00:01');
# End Session
UPDATE session SET `end` = CURRENT_TIMESTAMP WHERE `id` = 1 ;
# Find open sessions
SELECT id FROM session WHERE trackId = 1 AND end = '1970-01-01 00:00:01';


# User
CREATE TABLE user (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
appId VARCHAR(36),
deviceId VARCHAR(36),
created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP);


# Create a User
INSERT INTO user (`id`,`appId`,`deviceId`, `created`, `updated`) VALUES ( 0, UUID(), '40403F27-C335-4C79-8D16-574BB22A5544', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP );
# Obtain `trackId`
SELECT id FROM user WHERE deviceId = '40403F27-C335-4C79-8D16-574BB22A5544';
# Obtain `appId`
SELECT appId FROM user WHERE deviceId = '40403F27-C335-4C79-8D16-574BB22A5544';




-- 1498A25E-3E75-4F57-8C71-76329C8148B8
INSERT INTO user (`id`,`appId`,`deviceId`, `created`, `updated`) VALUES ( 0, UUID(), '1498A25E-3E75-4F57-8C71-76329C8148B8', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP );

#################################################
Device ID: 40403F27-C335-4C79-8D16-574BB22A5544

// Events
- Create a user with a `deviceId` -> `trackId`(INT) [user.id]
- Start a session using the `trackId`(INT) & `updateInterval`(DOUBLE) -> `sessionId` (INT)
- - Add Location and Heading updates using the `sessionId`(INT)
-- lookup sessions and provide session results.



####################
## Video Sections ##
####################

# Video
CREATE TABLE video (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
url VARCHAR(2083),
title VARCHAR(200),
created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP);

# Adding a bool to handle if it has been pulled or not,
ALTER TABLE video ADD COLUMN pulled TINYINT(1);

ALTER TABLE video ADD COLUMN downloaded TINYINT(1);

ALTER TABLE video ADD COLUMN downloadDate TIMESTAMP;

ALTER TABLE video ADD COLUMN pulledDate TIMESTAMP;

-- Adding A download verified column to track if the file was actually downloaded and not interupted but went through the loop and got marked as downloaded anyway... 
ALTER TABLE video ADD COLUMN downloadVerified TINYINT(1);
-- Set defaults on existing records.
UPDATE video SET downloadVerified = '0' WHERE downloadVerified IS NULL;



# 6-21-2019
## Star
CREATE TABLE star (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
url VARCHAR(2083),
title VARCHAR(200),
explorationDate TIMESTAMP NOT NULL DEFAULT '1970-01-01 00:00:01',
created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP);

# Using.. 

INSERT INTO star (`id`,`url`,`title`, `created`, `updated`) VALUES ( 0, "www.blah.com", 'blah', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP );

-- Find next star to explore
select * from star where explorationDate = '1970-01-01 00:00:01' order by created asc limit 1;

# start exploration using id
UPDATE star SET `explorationDate` = CURRENT_TIMESTAMP WHERE id = '1';


## User
CREATE TABLE user (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
userId INT,
name VARCHAR(200),
lastChecked TIMESTAMP NOT NULL DEFAULT '1970-01-01 00:00:01',
created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP);













