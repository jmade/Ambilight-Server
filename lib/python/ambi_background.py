import subprocess
from lib.python.dbutil import background_insert, last_kill_pid, current_light_status, set_light_status, light_info

# Light DB Helpers
def activate_lights(process_name:str):
	set_light_status('Y',process_name)
	return

def de_activate_lights():
	set_light_status('N','-')
	return

def db_check_for_lights() -> bool:
	status = current_light_status()
	if status == 'N':
		return True
	else:
		return False

def functional_light_check() -> bool:
	result = 0
	result += pid_query('ambi_loop')
	result += pid_query('_ambilight')
	if result > 0:
		return False
	else:
		return True

def light_reading() ->dict:
	return light_info()

def light_status() -> str:
	info = light_info()
	status = info['status']
	process = info['process']
	if status == 'Y':
		return 'Ambilight-System is Running: {0}'.format(process)
	else:
		return "Ambilight-System is Off."

def lights_are_off() -> bool:
	return functional_light_check()

def pid_query(process_name:str):
	out = subprocess.Popen(["pgrep", "-f", process_name],
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
	stdout,stderr = out.communicate()

	output = stdout.decode('utf-8')
	split_out = output.split("\n")
	filtered_out = [ int(x) for x in split_out if x != '' ]
	if len(filtered_out):
		return 1
	else: 
		return 0

def kill_process(process_name:str):
	out = subprocess.Popen(["pgrep", "-f", process_name],
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
	stdout,stderr = out.communicate()

	output = stdout.decode('utf-8')
	split_out = output.split("\n")
	pids = [ int(x) for x in split_out if x != '' ]

	if len(pids):
		kill_pid = max(pids)
		kill_out = subprocess.Popen(['bash', '/home/pi/Ambilight/lib/shell/kill.sh', str(kill_pid)])
		kill_out.communicate()


def start_loop():
	if lights_are_off():
		cmd = 'cd ~/rpi_ws281x/python && sudo PYTHONPATH=".:build/lib.linux-armv7l-2.7" python ~/Ambilight/lib/python/ambi_loop.py'
		process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
		kill_pid = str(int(process.pid) + 5)
		background_insert(kill_pid,'ambi_loop')
		activate_lights('ambi_loop')
	else:
		print("Light are reporting status: ON.")


def start_ambi():
	if lights_are_off():
		cmd = 'cd ~/rpi_ws281x/python && sudo PYTHONPATH=".:build/lib.linux-armv7l-2.7" python ~/Ambilight/lib/python/_ambilight.py'
		process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
		kill_pid = str(int(process.pid) + 5)
		background_insert(kill_pid,'ambi_light')
		activate_lights('ambi_light')
	else:
		print("Light are reporting status: ON.")

def start_blackout():
	cmd = 'cd ~/rpi_ws281x/python && sudo PYTHONPATH=".:build/lib.linux-armv7l-2.7" python ~/Ambilight/lib/python/blackout.py'
	process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)


def kill_loop():
	kill_process('ambi_loop')
	de_activate_lights()

def kill_ambilight():
	kill_process('_ambilight')
	de_activate_lights()



def stop_process(process_name:str):
	kill_process(process_name)
	de_activate_lights()

def start_process(process_name:str):
	if lights_are_off():
		cmd = 'cd ~/rpi_ws281x/python && sudo PYTHONPATH=".:build/lib.linux-armv7l-2.7" python ~/Ambilight/lib/python/{0}.py'.format(process_name)
		process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
		kill_pid = str(int(process.pid) + 5)
		background_insert(kill_pid,process_name)
		activate_lights(process_name)
	else:
		print("Light are reporting status: ON.")


