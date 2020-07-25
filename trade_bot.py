import collections
import json
import time
from collections import OrderedDict
import pandas as pd


def load_data():
    with open('data.json', 'r') as json_file:
        data = json.load(json_file, object_pairs_hook=OrderedDict)
        return data


class TradeBot(object):
    def __init__(self, determine_actions_function):
        self.determine_actions_function = determine_actions_function
        self.last_trade_ts = 0
        self.price_history = OrderedDict() # {assetA: [{ask, bid}, {ask2, bid2}]}
        self.trades = list()

    def write_trades(self):
        outfile_name = f'ori_trades_{int(time.time())%1000}.json'
        with open(outfile_name, 'w') as outfile:
            json.dump(self.trades, outfile, indent=1)
        return outfile_name

    def log_datapoint(self, prices):
        for asset, data in prices.items():
            if asset not in self.price_history.keys():
                self.price_history[asset] = collections.deque(maxlen=100)
            self.price_history[asset].append(data)

    def send_trade_command(self, actions, ts):
        self.trades.append({'time': ts, 'actions': actions})
        self.last_trade_ts = ts

    def make_trades(self, ts, prices):
        self.log_datapoint(prices)
        if ts - self.last_trade_ts < 30*1000:
            return

        actions = self.determine_actions_function(self)

        if actions:
            self.send_trade_command(actions, ts)


def rolling_avg_actions(self):
    window_size = 50
    actions = []
    for asset in self.price_history.keys():
        current_bid = self.price_history[asset][-1]['bid']
        current_ask = self.price_history[asset][-1]['ask']

        try:
            prev_bid = self.price_history[asset][-2]['bid']
            prev_ask = self.price_history[asset][-2]['ask']
        except IndexError:
            continue

        bid_series = pd.Series([point['bid'] for point in self.price_history[asset]])
        windows = bid_series.rolling(window_size)
        bid_moving_avgs = windows.mean()

        current_bma = bid_moving_avgs.iloc[-1]
        prev_bma = bid_moving_avgs.iloc[-2]

        ask_series = pd.Series([point['ask'] for point in self.price_history[asset]])
        windows = ask_series.rolling(window_size)
        ask_moving_avgs = windows.mean()

        current_ama = ask_moving_avgs.iloc[-1]
        prev_ama = ask_moving_avgs.iloc[-2]

        flag = 0
        if current_ask > current_ama and prev_ask < prev_ama:  # we crossed above the MA
            actions.append(f'buy{asset[-1]}')
            flag = 1

        if current_bid < current_bma and prev_bid > prev_bma:  # we crossed below the MA
            if flag:
                print("flag was set and went into second if clause")
            else:
                actions.append(f'sell{asset[-1]}')

    return actions


if __name__ == '__main__':
    bot = TradeBot(rolling_avg_actions)
    data = load_data()
    i = 0
    start = time.time()
    for ts, prices in data.items():
        print(f"Progress: {i/len(data)*100:.2f}%, elapsed: {time.time() - start:.2f}s")
        bot.make_trades(int(ts), prices)
        i+=1
    outfile = bot.write_trades()
    print(f"done trading, oufile written: {outfile}")
