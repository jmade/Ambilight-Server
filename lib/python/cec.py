import subprocess
from time import sleep


BASE_DIR = '/home/pi/Ambilight/Controls/CEC/'

def generate_cmd(script_name):
	return BASE_DIR+script_name+'.sh'

def executeCommand(script_name):
	subprocess.Popen(['bash', generate_cmd(script_name) ])
	
def hdmi_1():
	executeCommand('hdmi_1')

def hdmi_2():
	executeCommand('hdmi_2')

def hdmi_3():
	executeCommand('hdmi_3')

def tv_power_off():
	executeCommand('tv_off')

def tv_power_on():
	executeCommand('tv_on')
	sleep(2.0)
	executeCommand('hdmi_1')
