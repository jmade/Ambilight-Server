from time import sleep
import subprocess
import os


from subprocess import check_output


BASE_DIR = '/home/pi/Ambilight/Controls/CEC/'

def generate_cmd(script_name):
	return BASE_DIR+script_name+'.sh'

def executeCommand(script_name):
	subprocess.Popen(['bash', generate_cmd(script_name)])
	
def hdmi_1():
	executeCommand('hdmi_1')

def hdmi_2():
	executeCommand('hdmi_2')

def hdmi_3():
	executeCommand('hdmi_3')

def tv_power_off():
	executeCommand('tv_off')


def get_tv_power_state():
	cdm = 'echo pow 0 | cec-client -s -d 1'
	out = check_output(cdm, shell=True)
	lines = out.decode("utf-8").split("\n")
	power_status = lines[-1].split('power status: ')[0]
	print("TV POWER STATUS: ",power_status)



# echo tx 40 44 41 | cec-client -s -d 1

def tv_power_on():
	cmd = "echo 'Powering On' && (echo on 0 | cec-client -s -d 1) && echo 'sleeping a few' && sleep 5 && echo 'HDMI 1' && (echo 'tx 1F:82:10:00' | cec-client -s -d 1) &" 
	os.system(cmd)

	# os.system("echo 'on 0' | cec-client RPI -s")

	# "sleep 5 ; echo foo | sleep 5 ; echo first &"

	# echo 'second'; sleep 5; echo 'first';

	# "echo on 0 | cec-client -s -d 1; echo 'tx 1F:82:10:00' | cec-client RPI -s &"


	# os.system("echo on 0 | cec-client -s -d 1")

	# "(sleep 5; echo on 0 | cec-client -s -d 1) & "

	#  "echo 'tx 1F:82:10:00' | cec-client RPI -s"

	# echo pow 0 | cec-client -s -d 1

	# Input 1: echo tx 1F:82:10:00 | cec-client -s -d 1

	# TV Status: (sleep 5; echo pow 0 | cec-client -s -d 1) & 

	# Power Off = echo standby 0 | cec-client -s -d 1

	# # executeCommand('tv_on')
	# sleep(5.0)
	# executeCommand('hdmi_1')
	# sleep(1.0)
	# executeCommand('hdmi_1')
