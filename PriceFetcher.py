import httplib2
import json
import time
import threading
import unicodedata

class PriceFetcher:
    base_url = "https://www.bitstamp.net/api/v2/ticker/"
    running = False

    pairsToFetch = {
        'ripple': 'xrpusd',
        'bitcoin': 'btcusd',
        'ethereum': 'ethusd',
    }

    prices = {

    }

    def __init__(self, interval=1):
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True  # Daemonize thread
        thread.start()

    def run(self):
        running = True
        while running:
            for currencyKey in self.pairsToFetch.keys():
                print "fetching %s" % currencyKey
                self.prices[currencyKey] = self.fetchPrice(self.pairsToFetch[currencyKey])
            time.sleep(60)

            time.sleep(self.interval)

    def fetchPrice(self, pair):
            try:
                h = httplib2.Http()
                (resp, content) = h.request(self.base_url + pair, "GET", headers={'content-type': 'application/json'})
                response = json.loads(content)
                return response["last"]
            except ValueError as e:
                print "cant get price for pair %s" % (pair)

    def startFetching(self):
        if self.running:
            return
        running = True
        while running:
            for priceKey in self.pairsToFetch.keys():
                print "fetching %s" % priceKey
                self.prices[priceKey] = self.fetchPrice(self.pairsToFetch[priceKey])
            time.sleep(60)

    def stopFetching(self):
        self.running = False

    def getPrice(self, currency):
        return  self.prices[currency]

    def printPrices(self):
        for pairKey in self.pairsToFetch:
            print "Price for %s is %s" % (pairKey, self.prices[pairKey])

