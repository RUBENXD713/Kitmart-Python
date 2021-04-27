import websocket
from threading import Thread
import time
import sys
import json

import codecs


encoding ="utf-8"
nbytes = {
    'utf-8': 1,
    'utf-16': 2,
    'utf-32': 4,
}.get(encoding, 1)


def to_hex(t, nbytes):
    """Format text t as a sequence of nbyte long values
    separated by spaces.
    """
    chars_per_item = nbytes * 2
    hex_version = binascii.hexlify(t)
    return b' '.join(
        hex_version[start:start + chars_per_item]
        for start in range(0, len(hex_version), chars_per_item)
    )

data=""

def on_message(ws, message):
    print("*"*20)
    print(message)


def on_error(ws, error):
    print(error)
    pass


def on_close(ws):
    print("### closed ###")


def on_open(ws,topic,mensaje):
    data={"t":1,"d":{"topic":topic}}
    ws.send(json.dumps(data))
    data={"t":7,"d":{"topic":topic,"event":"message","data":mensaje}}
    ws.send(json.dumps(data))
    time.sleep(5)

    ws.close()
        #print("Thread terminating...")

    #Thread(target=run).start()

'''if __name__ == "__main__":
    websocket.enableTrace(True)
    if len(sys.argv) < 2:
        host = "ws://localhost:3333/ws"
    else:
        host = sys.argv[1]
    ws = websocket.WebSocketApp(host,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    
    ws.on_open = on_open


    ws.run_forever()'''

