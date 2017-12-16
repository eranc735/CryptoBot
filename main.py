import PriceFetcher
import time

if __name__ == "__main__":
        fetcher = PriceFetcher.PriceFetcher()
        #fetcher.startFetching()
        time.sleep(3)
        fetcher.printPrices()
        #fetcher.stopFetching()

