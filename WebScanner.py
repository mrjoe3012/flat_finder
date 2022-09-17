from abc import ABC, abstractmethod
import requests, re
from Property import *

# scans a website for properties
class WebScanner(ABC):
    def __init__(self):
        self.base_url = ""
        self.url = ""
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        self.re1 = ""

    # returns a list of properties
    def scan(self):
        properties = []

        response = requests.get(self.url, headers=self.headers)        
        response.raise_for_status()
        re1 = re.compile(self.re1)
        url_parts = re1.findall(response.text)
        for url_part in url_parts:
            id = url_part
            url = self.base_url + url_part
            if all([x.id != id for x in properties]):
                properties.append(Property(id, url))
        return properties

class RightMoveScanner(WebScanner):
    def __init__(self):
        super().__init__()
        self.url = "https://www.rightmove.co.uk/property-to-rent/find.html?minBedrooms=2&maxBedrooms=2&keywords=&sortType=6&includeLetAgreed=false&viewType=LIST&channel=RENT&index=0&maxPrice=1000&radius=3.0&maxDaysSinceAdded=1&locationIdentifier=REGION^93616"
        self.base_url = "https://rightmove.co.uk"
        self.re1 = 'propertyCard-link.*href="([^"]+)"'

class ZooplaScanner(RightMoveScanner):
    def __init__(self):
        super().__init__()
        self.url = "https://www.zoopla.co.uk/to-rent/property/2-bedrooms/glasgow-city-centre/?price_frequency=per_month&price_max=1000&q=Glasgow+City+Centre%2C+Glasgow&radius=3&search_source=refine&beds_min=2&added=24_hours"
        self.base_url = "https://zoopla.co.uk"
        self.re1 = 'href="(\/to-rent\/details\/[0-9]+\/[^"]+)"'