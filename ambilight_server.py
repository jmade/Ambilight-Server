from flask import Flask, jsonify, request, redirect, url_for
from time import sleep

from server_lib import pages

from lib.python.ambi_ir import hdmi_switch
from lib.python.atv import atv_remote
from lib.python.cec import hdmi_1, hdmi_2, hdmi_3, tv_power_on, tv_power_off
from lib.python.vol import volumeUp, volumeDown, volumeUpTriple, volumeDownTriple, volumeDownMax
from lib.python.ambi_background import start_loop, kill_loop, start_ambi, kill_ambilight, light_status, light_reading, start_blackout

from enum import Enum

class classproperty(object):
    def __init__(self, getter):
        self.getter= getter
    def __get__(self, instance, owner):
        return self.getter(owner)

class AppType(Enum):
    CEC = 'CEC'
    NEOPIXEL = 'Neopixel'
    VOLUME = 'Volume'
    ATV = 'ATV'
    IR = 'IR'
    TEST = 'TEST'
    EXP = 'EXPERIMENTAL'

    @classproperty
    def __values__(cls):
        return [m.value for m in cls]

# Color Helpers
RESET="\x1b[0;0m"
GREEN="\x1b[1;32m"
BOLD="\x1b[1m"
BLUE="\x1b[34m"
YELLOW="\x1b[93m"

app = Flask(__name__, static_folder='script')
app.config['SECRET_KEY'] = 'top-secret!'


# Response Dict
def request_ok(response_dict, success=True):
    response_dict.update({
        'success': success
    })
    resp = jsonify(**response_dict)
    resp.status_code = 200
    return resp


# HTML Responses
@app.route('/action',methods=['POST', 'GET'])
def action():
  if request.method == 'POST':
    action_value = request.form['action']
    if action_value is None:
        return request_ok({'message':'okay'})
    elif action_value == 'Color':
        color_string = request.form['color']
        return redirect(url_for('success_action',value=action_value))
    else:
        return redirect(url_for('success_action',value=action_value))
  else:
    return request_ok({'message':'okay'})


# Test Loop
@app.route('/test_loop',methods = ['POST', 'GET'])
def test_loop():
  if request.method == 'POST':
    user = request.form['nm']
    return redirect(url_for('success',name = user))
  else:
    user = request.args.get('nm')
    return redirect(url_for('success',name = user))


def makeIndexOptions():
    start_ambilight = False
    start_loop = False
    show_test = True
    if LOOP_PID == 0:
        start_loop = True
    if AMBI_PID == 0:
        start_ambilight = True
    return (start_ambilight,start_loop,show_test)

# Index
@app.route('/')
def index():
    return pages.index(makeIndexOptions())



# IR
def test_ir():
    press_button_1()

def switch_to_apple_tv():
    hdmi_switch(1)

def switch_to_nintendo_switch():
    hdmi_switch(2)

def switch_to_ps4():
    hdmi_switch(4)

def switch_to_input4():
    hdmi_switch(4)


# AppleTV

def atv_up():
    atv_remote('up')

def atv_down():
    atv_remote('down')

def atv_left():
    atv_remote('left')

def atv_right():
    atv_remote('right')

def atv_select():
    atv_remote('select')

def atv_menu():
    atv_remote('menu')

def atv_pause():
    atv_remote('pause')

def atv_top_menu():
    atv_remote('top_menu')


# App Responses

# Options response
def make_option_entry(title:str,cat:str,description='None'):
    return {
        'title' : title,
        'catagory' : cat,
        'description' : description,
    }

def option_entries():
    return [
        # make_option_entry(title='Watch Apple TV w/Ambilight',catagory=catE,description=''),
        make_option_entry(title='Ambilight ON',cat=AppType.NEOPIXEL.value,description='This action will start the Ambilight System to display the given input.'),
        make_option_entry(title='Ambilight OFF',cat=AppType.NEOPIXEL.value),
        make_option_entry(title='Neopixel Loop ON',cat=AppType.NEOPIXEL.value,description='Start a Demo Loop of the Neopixels on a Background Process.'),
        make_option_entry(title='Neopixel Loop OFF',cat=AppType.NEOPIXEL.value,description='Stop a Backgrounded Demo Loop of Neopixels.'),

        make_option_entry(title='Test',cat=AppType.TEST.value,description='Endpoint Test.'),

        make_option_entry(title='HDMI Input 2',cat=AppType.CEC.value,description='HDMI Input 2.'),
        make_option_entry(title='HDMI Input 3',cat=AppType.CEC.value,description='HDMI Input 3.'),

        make_option_entry(title='Select',cat=AppType.ATV.value,description='AppleTV Select via a Command being send on the server.'),
    ]

def options_dict() -> dict:
    return {
        'app_types' : AppType.__values__,
        'options' : option_entries(),
        'light_reading' : light_reading(),
    }


#  for the app 
def createOptionsResponse():
    return request_ok( {
        'options' : options_dict(),
    })


#################
# Server Routes #
#################

@app.route('/ping', methods=['GET', 'POST'])
def ping():
    return request_ok({
        'message': 'PONG'
    })

def emptyOption():
    print("Empty Option.")

def availibleActions():
    return {
        # Test
        'Test' : emptyOption,
        # HDMI CEC 
        'TV Power Off' : tv_power_off,
        'TV Power On' : tv_power_on,
        'HDMI 1' : hdmi_1,
        'HDMI Input 2' : hdmi_2,
        'HDMI Input 3' : hdmi_3,
        # Volume
        'Volume Up' : volumeUp,
        'Volume Down' : volumeDown,
        'Volume Up (3)' : volumeUpTriple,
        'Volume Down (3)' : volumeDownTriple,
        'Volume Down Max' : volumeDownMax,
        # IR
        'Apple TV' : switch_to_apple_tv,
        'Nintendo Switch' : switch_to_nintendo_switch,
        'PS4' : switch_to_ps4,
        'Input 4' : switch_to_input4,
        # Apple TV commands
        'Up' : atv_up,
        'Down' : atv_down,
        'Left' : atv_left,
        'Right' : atv_right,
        'Select' : atv_select,
        'Menu' : atv_menu,
        'Pause' : atv_pause,
        'Top Menu' : atv_top_menu,
        # 
        'Neopixel Loop ON' : start_loop,
        'Neopixel Loop OFF' : kill_loop,
        'Ambilight ON' : start_ambi,
        'Ambilight OFF' : kill_ambilight,
    }

@app.route('/chosen_action',  methods=['GET', 'POST'])
def chosen_action():
    print(BOLD+BLUE+'Ambilight System: '+RESET+YELLOW+light_status()+RESET)
   
    chosen_action = request.form['action']
    print(BOLD+YELLOW+"Chosen Action: "+RESET+GREEN+chosen_action+RESET)
    availibleActions()[chosen_action]()

    return request_ok({
        'result': chosen_action
    })


@app.route('/ambi_app',  methods=['GET', 'POST'])
def ambi_app():
    print("Mobile App - "+BOLD+YELLOW+"Options"+RESET)
    sleep(1.0)
    return createOptionsResponse()


@app.route('/test', methods=['GET', 'POST'])
def test():
    return request_ok({ 'message': 'Welcome to Amiblight\'s moblie API.'})


def run_app():
    app.run(debug=1.0,use_reloader=True, host='0.0.0.0', port=8080)
    
if __name__ == '__main__':
    run_app()