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

    def _getHTML(self):
        response = requests.get(self.url, headers=self.headers)        
        response.raise_for_status()
        return response.text

    # returns a list of properties
    def scan(self):
        properties = []

        
        re1 = re.compile(self.re1)
        html = self._getHTML()
        url_parts = re1.findall(html)
        for url_part in url_parts:
            id = url_part
            url = self.base_url + url_part
            if all([x.id != id for x in properties]):
                properties.append(Property(id, url))
        return properties

class RightMoveScanner(WebScanner):
    def __init__(self):
        super().__init__()
        self.url = "https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E93616&maxBedrooms=10&minBedrooms=1&maxPrice=1000&radius=3.0&propertyTypes=&maxDaysSinceAdded=1&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords="
        self.base_url = "https://rightmove.co.uk"
        self.re1 = 'propertyCard-link.*href="([^"]+)"'

class ZooplaScanner(RightMoveScanner):
    def __init__(self):
        super().__init__()
        self.url = "https://www.zoopla.co.uk/to-rent/property/2-bedrooms/glasgow-city-centre/?price_frequency=per_month&price_max=1000&q=Glasgow+City+Centre%2C+Glasgow&radius=3&search_source=refine&beds_min=1&added=24_hours&view_type=list"
        self.base_url = "https://zoopla.co.uk"
        self.re1 = 'href="(\/to-rent\/details\/[0-9]+\/[^"]+)"'

class OnTheMarkerScanner(RightMoveScanner):
    def __init__(self):
        super().__init__()
        self.url = "https://www.onthemarket.com/to-rent/1-bed-flats-apartments/glasgow-west-end/?max-price=1000&radius=4.0&recently-added=24-hours"
        self.base_url = "https://onthemarket.com"
        self.re1 = 'href="(\/details\/[^"]+)"'

class S1HomesScanner(RightMoveScanner):
    def __init__(self):
        super().__init__()
        self.url = "https://www.s1homes.com/rent/search/forrent_search_results.cgi?refine=1&verylocalstart=&area_id=&sortedby=&location=&minprice=0&maxprice=1000&bedrooms=1-3&bedroomsMin=1&bedroomsMax=3&type=Flat&availability=Any&furnished=&whenpropadded=1&keywords=&submit=&all="
        self.base_url = "https://www.s1homes.com"
        self.re1 = 'href="(\/Flats-for-rent\/[^"]+\.shtml)"'