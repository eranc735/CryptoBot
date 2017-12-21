import httplib2
import json
import time
import threading
import enum

class AlertType(enum.Enum):
    Upper = 1
    Lower = 2

class PriceAlert:
    def __init__(self, user, priceThreashold, boundaryType):
        self.user = user
        self.priceThreashold = priceThreashold
        self.boundaryType = boundaryType

    def isApplicable(self, price):
        if self.boundaryType == AlertType.Upper and self.priceThreashold > price:
            return False
        elif self.boundaryType == AlertType.Lower and self.priceThreashold > price:
            return True
        return False

class PriceFetcher:
    base_url = "https://www.bitstamp.net/api/v2/ticker/"
    running = False

    pairsToFetch = {
        'ripple': 'xrpusd',
        'bitcoin': 'btcusd',
        'ethereum': 'ethusd',
    }

    def __init__(self):
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True  # Daemonize thread
        thread.start()
        self.prices = {}
        self.priceAlerts = {}

    def run(self):
        running = True
        while running:
            for currencyKey in self.pairsToFetch.keys():
                print "fetching %s" % currencyKey
                price = self.fetchPrice(self.pairsToFetch[currencyKey])
                self.updatePrice(currencyKey, price)
            time.sleep(60)

    def addCAlert(self, currency, user, priceThreashold, alertType):
        if not currency in self.priceAlerts:
            self.priceAlerts[currency] = []
        alert = PriceAlert(user, priceThreashold, alertType)
        self.priceAlerts[currency].add(alert)


    def updatePrice(self, currency, price):
        self.prices[currency] = price
        if currency in self.alerts:
            priceAlerts = self.alerts[currency]
            for alert in priceAlerts:
                if alert.isApplicable(price):
                    self.sendPriceAlert("", alert)

    def sendPriceAlert(self, alert):
        print(alert.user)

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

