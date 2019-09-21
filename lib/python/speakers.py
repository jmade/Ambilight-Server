#from time import sleep
import os.path
from os import path, system
from lib.python.vol import volumeUp, volumeDown

FILE_LOCATION = '/home/pi/VOLUME'


# 192.168.0.8:8080/speaker/get

def speaker_action(action,request,amt=None):
	
	# Get Volume
	if action == 'get':
		return { 'volume' : get_volume() }

	# Set Volume
	if action == 'set':
		newValue = None if 'newValue' not in request.form else request.form['newValue']
		if newValue is None:
			return { 'volume' : get_volume() }
		else:
			set_volume(newValue)
			return { 'volume' : get_volume() }

	# Volume Up
	if action == 'up':
		return incrementVolume(1)

	# Volume Down
	if action == 'down':
		return decrementVolume(1)


	if action == 'muteOn':
		return { 'value' : 1 }
	if action == 'muteOff':
		return { 'value' : 0 }
	if action == 'muteStatus':
		return { 'value' : 0 }

	# Else
	return { 'volume' : get_volume() }


def incrementVolume(amount):
	current_volume = get_volume()
	newVolume = current_volume + amount
	set_volume(newVolume)
	volumeUp()
	return { 'volume' : get_volume() }

def decrementVolume(amount):
	current_volume = get_volume()
	newVolume = current_volume - amount
	set_volume(newVolume)
	volumeDown()
	return { 'volume' : get_volume() }




# Accessors
def get_volume():
	check_file()
	lines = []
	with open(FILE_LOCATION,'r') as file:
		lines = file.readlines()
	if len(lines):
		volume = lines[0]
		return int(volume)
	else: # No volume found... calibrate?
		calibrate()
		return 0

def set_volume(volume):
	with open(FILE_LOCATION,'w') as file:
		file.write(str(volume))

# Utility
def check_file():
	if path.isfile(FILE_LOCATION):
		return True
	else:
		calibrate()
		False


def calibrate():
	print("**Volume File Calibration**")
	# needs to spin the motor all the way down, several times and write volume at 0
	# make new file delte then save new volume file, then increment twice?... ???
	os.system('rm -rf '+FILE_LOCATION)
	print("File Deleted.")
	set_volume(0)
	print("Creating New File Setting Volume to 0")
	get_volume()



