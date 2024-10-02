#!/usr/bin/env python3
"""
240930 -  two streams (on port 5000 it can have independet labels via mqtt

watch -n 11 ' mosquitto_pub -t "telemetrix/widget1port5000Gamma" -m `awk "BEGIN { srand($RANDOM); print rand() * 3 }"`'

watch -n 30 ' mosquitto_pub -t "telemetrix/temp2" -m `awk "BEGIN { srand($RANDOM); print rand() * 100 }"` '


"""

from fire import Fire
from flashcam.version import __version__
from flashcam.mmapwr import mmwrite # for daq
from console import fg, bg
import os
from flashcam import config
import time
import datetime as dt
#
import tdb_io.influx as influx
import sys
import signal
import paho.mqtt.client as mqtt

import logging
import re



logging.basicConfig(
    filename=os.path.expanduser("~/flashcam_daq.log"),
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.INFO,

)
logger = logging.getLogger(__name__)


"""
The idea is
 1/ to take care about PORTS and PIPES, accept just a number (ideally)
 2/ use cfg.json to understand the number
 3/  PIPE is defined HERE like /tmp/flashcam_fifo_x001 ....
"""

PRIMARY_PORT = None # on startup - port is correct, with load_config - can change
MAX_PORTS = 6 # this is UNO+Shield limit to plugin

def test():
    #cmd_ls( ip = ip,db = i['name'], series="all", qlimit = qlimit, output =output)
    if influx.check_port() :
        print("i... influx port present localy")
        commavalues = "a=1,b=2"
        influx.influxwrite( DATABASE="local", MEASUREMENT="flashcam",
                 values=commavalues,
                 IP="127.0.0.1"
                 )
    sys.exit(0)


def is_int(n):
    if str(n).find(".")>=0:  return False
    if n is None:return False
    try:
        float_n = float(n)
        int_n = int(float_n)
    except ValueError:
        return False
    else:
        return float_n == int_n



import socket
import threading

def is_float(n):
    if n is None:return False
    try:
        float_n = float(n)
    except ValueError:
        return False
    else:
        return True


########################################################
#
#   recalculate if flashcam knows the calib system.... TEMP_phid HUMI_phid
#
######################################################3

def recalibrate(d, title ):
    """
    d comes as string BUT is sure it is a number; whatever happens, return rounded thing
    """
    res = d
    newtitle = title
    logger.info(f"D...RECAL  {d} ... {type(d)}   /{float(d)}/    /{title}/ ")
    print(f"D... Before : {d}  ->   /{float(d)}/    /{title}/ ")
    # *********************************
    if title.endswith("TEMP_phid"):
        res = round( float(d) / 1024* 222.2 - 61.111, 1)
        if title != "TEMP_phid": newtitle = title.replace("TEMP_phid", "")
    # ************************************
    elif title.endswith("HUMI_phid"):
        res = round( float(d) / 1024* 190.6 - 40.2, 1)
        if title != "HUMI_phid": newtitle = title.replace("HUMI_phid", "")
    # ********************************************************************** END
    else:
        res = round( float(d), 1)
    print(f"D... After  :  {res}   {type(res)}  ")
    if newtitle[-1] == "_" and len(newtitle) > 2:
        newtitle = newtitle[:-1]
    logger.info(f"D...RECALfin  {res} ... {newtitle}")
    return res, newtitle


# #########################################################################
#
#                      Process DATA
#
#############################################################################
def process_data(data, index, CAM_PORT, OVR_LABEL=None):  #no OVR_LABEL!~!!!!
    """
    fit the incomming data into the format template
    AND - possibly recalculate raw data :)!
 "mminput1_cfg": "dial xxx;22;28;5;signal1",
 "mminput2_cfg": "dial xxx;22;28;5;dial2",
 "mminput3_cfg": "dial xxx;22;28;5;tacho3",
 "mminput4_cfg": "dial xxx;22;28;5;box4",
 "mminput5_cfg": "sub xxx;22;28;5;title5"

    """
    global PRIMARY_PORT
    # DATA ---------------------------
    d = None
    try:
        d = data.decode('utf8').strip()
    except:
        d = str(data).strip()
    print(f"i...  {bg.wheat}{fg.black}   receivd: /{d}/  on index /{index}/ CAMPORT={CAM_PORT} {bg.default}{fg.default}")
    #logger.info(f"D...  PDa receivd: /{d}/  on index {index} ")

    # without port - they are normal mminput1 and  mminput1_cfg # ************************
    item_file = f"mminput{index}"
    item_cfg = f"mminput{index}_cfg"
    if PRIMARY_PORT != CAM_PORT: # one more set of conncetors defined in config
        item_file = f"mminput{index+10}"
        item_cfg = f"mminput{index+10}_cfg"

    if not item_file in config.CONFIG:
        print(fg.red, f"X... MMAP file {index} - {item_file} not defined in {config.CONFIG['filename']}  ",  fg.default)
        return
    if not item_cfg in config.CONFIG:
        print(fg.red, f"X... template {index} - {item_cfg} not defined in {config.CONFIG['filename']}  ",  fg.default)
        return

    mmfile = config.CONFIG[ item_file ]
    mmtemplate = config.CONFIG[item_cfg ]

    # ------------------  MMAP file and TEMPLATE defined from here ======================================


    # prepare recalibration, you need to know title/label ....... Also - IF  number => write to INFLUX
    #
    if is_float(d) or is_int(d):
        # extract LABEL/TITLE that is crutial for recalibration
        mytitle = " ".join(mmtemplate.split(" ")[1:]).split(";")[4]

        #if OVR_LABEL is None: # MQTT  override label
        #    #  recalibrate by label
        d, newtitle= recalibrate( d, mytitle ) #  d goes as string returns as float
        #else:
        #    # no recal!
        #    d, newtitle= recalibrate( d, "placeholder" ) #  d goes as string returns as float

        #if OVR_LABEL is not None: newtitle = OVR_LABEL
        #mmtemplate = mmtemplate.replace(mytitle, newtitle ) # FIT THE DATA INTO THE FIELD

        mmtemplate = mmtemplate.replace("xxx", str(d) ) # FIT THE DATA INTO THE FIELD
        #print(f"DEBUG4 {d} ### {mmtemplate} ", flush=True)
        logger.info(f"D...  mmwrite: {mmtemplate}  ")
        # *******************
        mmwrite( mmtemplate, mmfile, debug=True, PORT_override=CAM_PORT )
        # *******************
        print(f"i... SUCCESS  MMWRITE ----- #{CAM_PORT}#  ", bg.white, fg.black, mmtemplate, fg.default, bg.default)

        if influx.check_port():
            #print("i... influx port present localy")
            #if OVR_LABEL is not None: #  override label
            #    commavalues = f"{OVR_LABEL}={d}"
            #else:
            commavalues = f"{mytitle}={d}"
                #if CAM_PORT != PRIMARY_PORT: # RECALIBRATION AND TRUNC Only for main port.....
                #    commavalues = f"{mytitle}_{CAM_PORT}={d}"
            try:
                influx.influxwrite( DATABASE="local",
                                    MEASUREMENT=f"flashcam{CAM_PORT}",
                                    values=commavalues,
                                    IP="127.0.0.1" )
                print(f"i... OK      WRITING  INFLUX => DB:flashcam{CAM_PORT}  ")
                logger.info(f"D...  PDa  InOK /{commavalues}/  on index {index} ")
            except:
                logger.info(f"D...  PDa  InXX /{commavalues}/  on index {index} ")
                print("X... ERROR  WRITING  INFLUX")

    else:# if not float.... make it a box and dont write INFLUX
        mmtemplate = mmtemplate.replace("xxx", d ) # FIT THE DATA INTO THE FIELD
        mmtemplate = mmtemplate.replace("signal", "box" )
        mmtemplate = mmtemplate.replace("dial", "box" )
        mmtemplate = mmtemplate.replace("tacho", "box" )
        logger.info(f"D...  MMAP  /{mmtemplate}/  on index {index} ")
        # *****************
        mmwrite( mmtemplate, mmfile, debug=False, PORT_override=CAM_PORT )#PRIMARY_PORT) # this is a uniquZ
        #
        print(f"i... SUCCESS  MMWRITE ----- #{CAM_PORT}# noINFLUX ", bg.white, fg.black, mmtemplate, fg.default, bg.default)
    print("_____________________________________", dt.datetime.now() )
    pass

############################################################3
#
#
#
#
##############################################################

def serve_port( PORT, TCP=True):
    """
    PORTS ********************************
    watch on PORT
    """
    global PRIMARY_PORT
    PRIMARY_PORT = int(config.CONFIG['netport'])
    s = None
    if TCP:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    ok = False
    try:
        s.bind(('0.0.0.0', PORT))  # Replace 12345 with your port number
        ok = True
    except:
        print(f"X... {bg.orange}{fg.black} DaQ PORT NOT ALLOCATED {PORT} {bg.default}{fg.default} ")

    if not ok:
        try:
            time.sleep(6)
            if TCP:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            else:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('0.0.0.0', PORT))  # Replace 12345 with your port number
            ok = True
        except:
            print(f"X...   {bg.red} DaQ PORT NOT ALLOCATED {PORT} {bg.default} ")

    if not ok: return
    s.listen(5)
    print(f"i...   {bg.blue} Data Acquisition Server started on port {PORT} ;  TCP{TCP} / UDP{not TCP}  {bg.default}")
    while True:


        conn, addr = s.accept() # I hope this is waiting, else 12% of procssor taken by load_config
        with conn:
            data = conn.recv(1024)
            if data:
                config.load_config()
                print(f'i...  {fg.blue}port data Received: {data};  config reloaded{fg.default}')
                # create index in place ; communication port
                process_data(data, PORT - int(PRIMARY_PORT), CAM_PORT=int(PRIMARY_PORT) )


# ************************************************************************
#
# NAMED PIPES
#
# ************************************************************************

def watch_named_fifo(PORT, fifon = '/tmp/flashcam_fifo'):
    """
    NAMED PIPES ************
    In client - use `os.path.exists` to check if the named pipe exists and `os.open` with `os.O_NONBLOCK` to check if it's open:
    """
    global PRIMARY_PORT
    fifoname = f"{fifon}_{PORT}"
    print(f"i...   {bg.darkgreen} Data Acquisition PIPE  started on {fifoname}   {bg.default}")
    if not os.path.exists(fifoname):
        os.mkfifo(fifoname)
    # Wait for the named pipe to be created
    #while not os.path.exists(fifo):
    #    time.sleep(1)
    with open(fifoname, 'r') as fifo_file:
        while True:
            data = fifo_file.readline().strip() # get what comes to PIPE
            if data:
                logger.info(f"*** fifo-readline data=={data} on PORT {PORT} ")
                print(f'i... {fg.green}named pipe Received: {data};  reloading config{fg.default}')
                config.load_config()
                #
                process_data(data, PORT - int(PRIMARY_PORT), CAM_PORT=int(PRIMARY_PORT) )
                time.sleep(0.1) # it runs all time.......
            else:
                time.sleep(0.1) # it runs all time.......





# ************************************************************************
#
#                                              MQTT --------------------
#
# ************************************************************************

def extract_numbers(s, topic="flashcam_daq"): # JUST widget and port
    #match = re.match(fr'^{topic}/widget(\d+)port(\d+)([A-Za-z]*)$', s)
    match = re.match(fr'^{topic}/widget(\d+)port(\d+)$', s)
    #print("D... ... matching ", match, s)
    if match:
        num1, num2 = match.groups()
        #print( match.groups() )
        return int(num1), int(num2) #, label if label else "dial"
    return None


# Define the callback for when a message is received
def mqtt_on_message(client, userdata, msg):
    global PRIMARY_PORT
    data = msg.payload.decode()
    #print(f"D... MQTT.Received message '{msg.payload.decode()}' on topic '{msg.topic}'")
    logger.info(f"*** mqtt         data=={data} on /{msg.topic}/ ")
    print(f"i... MQTT       {fg.violet}Received: {data};  on topic '{msg.topic}' rel-config {fg.default}")
    config.load_config()
    result = extract_numbers(msg.topic, topic="flashcam_daq")     #= 'flashcam_daq/widget3port5000'
    if result:
        widget, port = result
        #print(f"D....    processing widget {widget} to port {port}  ********************************************")
        process_data(data, widget, CAM_PORT=port )      #PORT - int(PRIMARY_PORT))
        pass
        #print("Format is correct. Numbers are:", result)
    else:
        print(f"X... {fg.red}MQTT Format is NOT widgetXportY {result}  {fg.default}")
    #    if msg.topic == "telemetrix/temp2":
    #        process_data(data, 3, CAM_PORT=PRIMARY_PORT)      #PORT - int(PRIMARY_PORT))



def mqtt_on_disconnect(client, userdata, rc):
    print("Disconnected. Attempting to reconnect...")
    try:
        client.reconnect()
    except Exception as e:
        print(f"Reconnection failed: {e}")


def watch_mqtt(POPO, MACHINE="127.0.0.1", PORT=1883):
    """
    MQTT  ************

    """
    fifoname = f"notnow_{PORT}"
    print(f"i...   {bg.violet} Data Acquisition MQTT started on {fifoname}   {bg.default}")

    # Create an MQTT client instance
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    # Assign the on_message callback
    client.on_message = mqtt_on_message
    client.on_disconnect = mqtt_on_disconnect

    # Connect to the broker
    client.connect( MACHINE, PORT, 60)

    # Subscribe to a topic
    client.subscribe("flashcam_daq/#")
    print(f"i...   {bg.violet} ... subscribing  flashcam_daq/#   {bg.default}")
    #client.subscribe("telemetrix/#")
    #client.subscribe("telemetix/temp2")

    # Start the loop to procss network traffic and dispatch callbacks
    client.loop_forever()



# ***************************************************
# ***************************************************
#
#
#
# ***************************************************
# ***************************************************

def main():
    """
    I have :
    PORTS
    and
    NAMED PIPES
    and
    MQTT

    """
    global PRIMARY_PORT
    PRIMARY_PORT = int(config.CONFIG['netport'])
    print()
    def signal_handler(sig, frame):
        print("Exiting with signal handler @bin...")
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    # *****************************************************************
    print("D... daq command - starting servers - start separatelly in FG")
    daq_threads = []
    for i in range(MAX_PORTS ):  # 012345 for 6UNO
        P = int(PRIMARY_PORT) + i + 1 #1-7  resp 8001-8007
        print(f"D...   starting server {i} - port {P} *****************")
        daq_threads.append( threading.Thread(
            target=serve_port,  args=( P, )  )  )
        #config.daq_threads[i].daemon = True
        daq_threads[i].start()

    #*****************************************************************
    print("D... daq command - starting PIPES - start separatelly in FG")
    daq_threads_FF = []
    for i in range(MAX_PORTS ): # 012345 for 6UNO
        P = int(PRIMARY_PORT) + i + 1
        print(f"D...   starting PIPE {i} - port {P} ********************")
        daq_threads_FF.append( threading.Thread(
            target=watch_named_fifo,  args=( P, )  )  )
        #config.daq_threads[i].daemon = True
        daq_threads_FF[i].start()

    #print(fg.violet)
    mqtt_thread = threading.Thread(
        target=watch_mqtt,  args=( P, )  )
    mqtt_thread.start()

    print("****************************** all prepared ")

    # ************************************************ JOIN ALL AT THE END
    for i in range(MAX_PORTS ): # 012345 for 6UNO
        daq_threads[i].join()
        daq_threads_FF[i].join()
        mqtt_thread.join()
    exit(0)

if __name__ == "__main__":
    Fire(test)
    Fire(main)
