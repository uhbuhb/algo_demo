# algo_demo

To install reqs just pipenv install.
With the pipenv activated, to run:

Task1:
python trade_bot.py 

Task2:
python price_logger.py

# Task description:
## Trading home task

The task is to write an automated strategy that reads a stream of timestamped ask/bid quotes of two assets, and outputs a series of trades in order to generate profit.

### Files included

data.json - includes timestamped ask/bid quotes of two assets.
output.json - includes an example of a series of trades in the required format.
evaluator.js - a nodejs script to evaluate output files and calculate their profit. (You can either run it, or review it to understand how the evaluation of trades is calculated).

### Task 1

Write a strategy to generate a trading series. You can use the evaluator to test it (with `node evaluator.js`) or write your own in whatever language. Consider:

* Treat data.json as a stream to be process in real time - i.e. every trade you 'execute' for a timestamp should be a result of the data the preceded that timestamp.
* To simulate the changing order book, trades should not be within 30 seconds of each other. (The evaluator will throw an error in case of a violation).
* Assume that every order is of size 1.

On top of the resulting process, add your thoughts of the following points:

* What are the differences between running such a trading simulation and real world trading?
    1. In real world wouldn't necessarily get an immediate fill. Would need to design some type of failure strategy 
    (which could actually improve performance as well because I could put submit somewhere between the bid/ask prices 
    hopefully get a better fill on both sides, or I would discover which direction the asset was progressing and that 
    possibly also improve my decisions).
    2. In real world I would have a ton of other data which I could use to analyse (evaluation, news, etc) which I could
    use to improve my decision making. Would need to optimise analysis of all the data as well.
    3. Definitely should improve runtime/speed of calculation. 
* How would you improve your strategy given more time/resources?
    1. The strategy I implmented is a simple "when prices crosses above 50 moving average buy, when it crosses below sell". 
    There are literally millions of strategies which could improve on this strategy which inclue other technical analysis
    or statistical price points, if you believe technical analysis is a successful way to trade the market, including 
    bollinger bands, crosses between different window length moving averages, etc etc.
    2. For this specific task, technical/statistical analysis is really the only thing I have to work with, because 
    the assets are theoretical assets so it would be impossible to do any other type of evaluation (fundamental, news 
    based, analyst ratings, volume, insider trading, etc), so that was the strategy I implemented. 
    3. It could be useful to check for some type of correlation between the 2 asset prices, on the assumption that a 
    rising tide raises all ships, and then trigger buy/sell commands a bit more conservatively (ie buy only if BOTH/aLL 
    assets are on the rise), or something like that.
    4. Could add some type of algo on the bid/ask spread with the assumption that the spread would get smaller (would 
    need to backtest this to check if it was the case), or either way there could be some patter which could be identified.

* How would the strategy differ given three assets? Four assets? N assets?
    1. If I had more assets to compare I would definitely want to check for correlation between them and then finetune 
    the strategy accordingly.
    2. I didnt touch anything that has to do with size of holdings.. with more asset to play with I could diversify risk
    a bit.
    
    
### Task 2

1. Write a simple program that connect to exchanges via (public) websocket, subscribes to required topics in order to write the data every second:
    + Done: ```python price_logger.py```
    + Notes:
        * I didnt print out exactly the requested columns, I wasn't able to 100% get the bid/ask/size/price on all exchanges,
        and it seemed to be different in each one, so instead of wasting a ton of time perusing the different APIs I did a 
        'best effort in decent amount of time' and just printed what I was able to collect. 
        * Im also not 100% clear on the different markets (there were so many here, many of which seemed to be 
        crypto/currency)... Given some guidance and some time this shouldn't be difficult.
2. add a new column, “mid price 1 hour ago” which writes the mid price ((ask+bid)/2) of each market, exactly 1 hour ago.
    * This I didn't do and would require a bit of a refactor to the price loggers I wrote because as is they dont save the 
the history they just log and forget. It wouldn't be difficult to implements this, if the point of the task is to demo 
quality of code I think this and the previous task covered that.
3. choose 1 exchange and subscribe to trades from the chosen exchange. print them as well alongside the orderbook data.
    * This would just require writing another price logger, subscribing to another websocket, and doing a bit of data 
    manipulation to combine the output.. Didn't have enough time to implement. 
4. question: what new information can you learn about the orderbook updates, based on the data in these trades. how could you improve the accuracy of the orderbook updates based on this new information?
    * I dont exactly understand the rest of these questions, so I stopped out here. Hopefully this will be enough in 
    for a take home project. 
    * Like I said on the phone, my experience is mostly in trading options on individual stocks 
    and I think there is a ton of potential there  to take advantage of in algotrading, as in addition to all the standard trading
    strategies, there is proven statistical advantage to be had, and I bring a deep knowledge of this field which 
     I would be super interested in pursuing.
5. implement an improved “orderbook” feed based on this data (you can print in high time resolution to show the effect).
    * Pass
6. question: what can be the problems when using this additional data? how would you overcome these problems?
    * Pass