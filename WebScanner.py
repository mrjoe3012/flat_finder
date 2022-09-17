from abc import ABC, abstractmethod
import requests, re
from Property import *

# scans a website for properties
class WebScanner(ABC):
    def __init__(self):
        pass

    # returns a list of properties
    @abstractmethod
    def scan(self):
        pass

class RightMoveScanner(WebScanner):
    def __init__(self):
        self.url = "https://www.rightmove.co.uk/property-to-rent/find.html?minBedrooms=2&maxBedrooms=2&keywords=&sortType=6&includeLetAgreed=false&viewType=LIST&channel=RENT&index=0&maxPrice=1000&radius=1.0&maxDaysSinceAdded=1&locationIdentifier=REGION%5E93616"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        # looks for the links to the properties in the search
        self.re1 = 'propertyCard-link.*href="([^"]+)"'
        # looks for the property id within the line
        self.re2 = '/([0-9]+#)/'

    def scan(self):
        properties = []

        response = requests.get(self.url, headers=self.headers)        
        response.raise_for_status()
        re1 = re.compile(self.re1)
        url_parts = re1.findall(response.text)
        for url_part in url_parts:
            re2 = re.compile(self.re2)
            id = re2.findall(url_part)
            url = "https://www.rightmove.co.uk" + url_part
            if all([x.id != id for x in properties]):
                properties.append(Property(id, url))
        #print("RightMoveScanner: Found {0} properties: {1}".format(len(properties), [str(x) for x in properties]))
        return properties