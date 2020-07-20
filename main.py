import dde_client as ddec
import time
import redis
import json
import os
import sys
from dotenv import load_dotenv
load_dotenv()
sys.setrecursionlimit(10000000)

# Connect to MT4
# Must register BID and ASK as topics separately..
QUOTE_client = ddec.DDEClient('MT4', 'QUOTE')

# Connect to Redis
r = redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), db=0)

# Register desired symbols..
symbols = os.getenv("SYMBOL").split(",")
for i in symbols:
    QUOTE_client.advise(i)

dictSymbol = {}
for s in symbols:
    dictSymbol[s] = {
        "bid": 0,
        "ask": 0 
    }

# Prove it worked:
columns = ['Symbol', 'DATE', 'TIME', 'BID', 'ASK']

print symbols

while 1:
    time.sleep(1)
    to_display = []
    for item in symbols:
        try:
            current_quote = QUOTE_client.request(item).split()
            symbol_dict = dictSymbol.get(item)
            print current_quote
            
            if(symbol_dict["bid"] != current_quote[2] or symbol_dict["ask"] != current_quote[3]):
                # Push Data
                
                # Save data
                dictSymbol[item]["bid"] = current_quote[2]
                dictSymbol[item]["ask"] = current_quote[3]
                # current_quote.insert(0, item)
                # to_display.append(current_quote)
                test_list = current_quote
                test_list.insert(0, item)
                print test_list
                pub = {
                    "symbol": item,
                    "bid": dictSymbol[item]["bid"],
                    "ask": dictSymbol[item]["ask"]
                }

                r.publish('quote', json.dumps(pub))
        except Exception, e:
            print "somethin went wrong: " + str(e)