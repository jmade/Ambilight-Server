from lib.python.dblib import call_sp, call_sql

# SELECT * FROM `background` ORDER BY id DESC LIMIT 1
# SELECT `pid` FROM `background` ORDER BY id DESC LIMIT 1;

def background_insert(pid,jobName):
	sp = "CALL sp_InsBackground('{0}','{1}')".format(pid,jobName)
	return call_sp(sp)

def last_kill_pid():
	sql_result = call_sql("SELECT `pid` FROM `background` ORDER BY id DESC LIMIT 1;")
	if len(sql_result):
		result_dict = sql_result[0]
		pid = result_dict['pid']
		return pid
	else:
		return {'Result':sql_result}


def set_light_status(status:str,proc_name:str):
	sp = "CALL sp_InsLightStatus('{0}','{1}')".format(status,proc_name)
	return call_sp(sp)

def light_info():
	sql_result = call_sql("SELECT `active`,`process` FROM `lightStatus` ORDER BY id DESC LIMIT 1;")
	if len(sql_result):
		result_dict = sql_result[0]
		status = result_dict['active']
		process = result_dict['process']
		return {'status':status,'process':process}
	else:
		return {'Result':sql_result}

def current_light_status():
	sql_result = call_sql("SELECT `active` FROM `lightStatus` ORDER BY id DESC LIMIT 1;")
	if len(sql_result):
		result_dict = sql_result[0]
		status = result_dict['active']
		return status
	else:
		return {'Result':sql_result}