import json
import time
import requests
import websocket

WS_EP = "wss://www.bitmex.com/realtime"

basic_command = {"op": "<command>", "args": ["arg1", "arg2", "arg3"]}


def subscribe_to_markets(ws):
    ws.send(json.dumps({"op": "subscribe", "args": ['instrument']}))


def process_received_data(ws):
    while True:
        msg = json.loads(ws.recv())
        if msg.get('info', None):
            print(f"received messge: {msg}")
            continue
        if msg.get('subscribe', None):
            assert msg['success']
            print(f"subscribed: {msg}")
            continue
        for data in msg['data']:
            print(f"data keys: {data.keys()}")
            try:
                print(f"{int(time.time())}, bitmex, {data['symbol']}, {data.get('prevPrice24h', '')}, {data.get('lastPrice', '')}, {data.get('markPrice', '')}")
            except KeyError:
                print(f"keyerror on message: {data}")


def log_data():
    ws = websocket.WebSocket()
    ws.connect(f'{WS_EP}')
    msg = json.loads(ws.recv())
    assert msg['info'].startswith('Welcome')
    subscribe_to_markets(ws)
    process_received_data(ws)


if __name__ == '__main__':
    log_data()
