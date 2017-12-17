import PriceFetcher
import time
import os
import re

if __name__ == "__main__":
        print os.environ['SLACKBOT']
        f = 5
        #fetcher = PriceFetcher.PriceFetcher()
        #fetcher.startFetching()
        #time.sleep(3)
        #fetcher.printPrices()
        #fetcher.stopFetching()
        GET_PRICE_COMMAND = r"get price of ([a-zA-Z]+)"
        matches = re.search(GET_PRICE_COMMAND, "get price of RIPPLE")
        vok = 5

