import json
import time

import requests
import websocket

REST_EP = 'https://ftx.com/api/'
WS_EP = "wss://ftx.com/ws/"


def send_ping(ws):
    ws.send(json.dumps({'op': 'ping'}))


def get_markets():
    res = requests.get(f'{REST_EP}/markets')
    assert res.status_code == 200
    res_json = res.json()
    markets = [entry['name'] for entry in res_json['result']]
    return markets


def subscribe_to_markets(ws, markets):
    for market in markets:
        ws.send(json.dumps({'op': 'subscribe', 'channel': 'trades', 'market': market}))


def iterate_data(ws):
    while True:
        response = json.loads(ws.recv())
        if response['type'] == 'subscribed':
            continue
        if response['type'] == 'pong':
            continue
        if response['type'] == 'update':
            for response_data in response['data']:
                data = f"{int(time.time())}, FTX, {response['market']}, {response_data['price']}, {response_data['size']}"
                ws.send(json.dumps({'op': 'ping'}))
                yield data


def log_data():
    markets = get_markets()

    ws = websocket.WebSocket()
    ws.connect(f'{WS_EP}/markets')
    ws.send(json.dumps({'op': 'ping'}))
    msg = ws.recv()

    subscribe_to_markets(ws, markets)

    for data in iterate_data(ws):
        print(data)


if __name__ == '__main__':
    log_data()

