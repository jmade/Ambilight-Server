import subprocess

BASE_DIR = '/home/pi/Ambilight/Controls/Commands/'

def generate_cmd(script_name):
	return BASE_DIR+script_name+'.sh'

def executeCommand(script_name):
	subprocess.Popen(['bash', generate_cmd(script_name) ])

def executeCommandMany(script_name):
	subprocess.Popen(['bash', generate_cmd(script_name), '2' ])

def executeCommandSeveral(script_name):
	subprocess.Popen(['bash', generate_cmd(script_name), '7' ])

def power():
	executeCommand('power')

def volume_up():
	executeCommand('volume_up')

def volume_down():
	executeCommand('volume_down')

def volume_up_many():
	executeCommandMany('volume_up')

def volume_down_many():
	executeCommandMany('volume_down')

def volume_up_several():
	executeCommandSeveral('volume_up')

def volume_down_several():
	executeCommandSeveral('volume_down')