# Import the module
import subprocess

def start_loop():
	# process = subprocess.Popen("bash /home/pi/Ambilight/lib/shell/strip.sh", shell=True, stdout=subprocess.PIPE)
	process = subprocess.Popen('cd ~/rpi_ws281x/python && sudo PYTHONPATH=".:build/lib.linux-armv7l-2.7" python ~/Ambilight/lib/python/ambi_loop.py', shell=True, stdout=subprocess.PIPE)
	print(process.__dict__)
	print("Started Ambi_Loop")
	print(process.pid)
	kill_pid = int(process.pid) + 1
	print("Kill PID: "+str(kill_pid))
	print("sudo kill -2 "+str(kill_pid))
	return kill_pid

start_loop()