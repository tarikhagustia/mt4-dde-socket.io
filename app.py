from win_func import WinMSGLoop
import dde_client_new as ddec
import redis
import os
import json
from dotenv import load_dotenv
load_dotenv()
import logging
class MyDDE(ddec.DDEClient):

    def set_redis(self, redis):
        self.redis = redis

    def callback(self, value, item=None):
        """Callback function for advice."""
        quote_array = value.split()
        quote = {
            "symbol" : item,
            "bid": quote_array[2],
            "ask": quote_array[3]
        }
        print quote
        self.redis.publish("quote", json.dumps(quote))

if __name__ == '__main__':
    dde = MyDDE("MT4", "quote")

    # Connect to Redis
    r = redis.Redis(host=os.getenv("REDIS_HOST"),
                    port=os.getenv("REDIS_PORT"), db=0)

    dde.set_redis(r)
    symbols = os.getenv("SYMBOL").split(",")
    for i in symbols:
        dde.advise(i)

    WinMSGLoop()