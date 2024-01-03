from abc import ABC, abstractmethod
import requests, re
from Property import *

# scans a website for properties
class WebScanner(ABC):
    def __init__(self):
        self.base_url = ""
        self.url = ""
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'}
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
        self.url = "https://www.rightmove.co.uk/property-to-rent/find.html?searchType=RENT&locationIdentifier=STATION%5E4394&insId=1&radius=3.0&minPrice=&maxPrice=1000&minBedrooms=1&maxBedrooms=&displayPropertyType=&maxDaysSinceAdded=1&sortByPriceDescending=&_includeLetAgreed=on&primaryDisplayPropertyType=&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=&letType=&letFurnishType=&houseFlatShare="
        self.base_url = "https://rightmove.co.uk"
        self.re1 = 'propertyCard-link.*href="([^"]+)"'

class ZooplaScanner(RightMoveScanner):
    def __init__(self):
        super().__init__()
        self.url = "https://www.zoopla.co.uk/to-rent/property/station/rail/haymarket/?added=24_hours&beds_min=1&price_frequency=per_month&price_max=1000&q=Haymarket%20Station%2C%20Edinburgh&radius=3&results_sort=newest_listings&search_source=to-rent"
        self.base_url = "https://zoopla.co.uk"
        self.re1 = 'href="(\/to-rent\/details\/[0-9]+\/[^"]+)"'

class OnTheMarkerScanner(RightMoveScanner):
    def __init__(self):
        super().__init__()
        self.url = "https://www.onthemarket.com/to-rent/property/haymarket-station/?let-length=long-term&max-price=1000&min-bedrooms=1&prop-types=bungalows&prop-types=detached&prop-types=farms-land&prop-types=flats-apartments&prop-types=mobile-park-homes&prop-types=semi-detached&prop-types=terraced&radius=3.0&recently-added=24-hours"
        self.base_url = "https://onthemarket.com"
        self.re1 = 'href="(\/details\/[^"]+)"'

class S1HomesScanner(RightMoveScanner):
    def __init__(self):
        super().__init__()
        self.url = "https://www.s1homes.com/rent/search/forrent_search_results.cgi?refine=0&veryLocal=779&verylocals=&bedrooms=1&keywords=&location=178&locationText=Haymarket%2C+City+Centre+%28Edinburgh%29&minprice=0&maxprice=1000&bedroomsMin=1&type=&btnSearch="
        self.base_url = "https://www.s1homes.com"
        self.re1 = 'href="(\/Flats-for-rent\/[^"]+\.shtml)"'

class TayLettingsScanner(RightMoveScanner):
    def __init__(self):
        super().__init__()
        self.url = "https://www.tayletting.co.uk/property/?wppf_max_bedrooms=3&wppf_max_rent=1000&wppf_branch=smepro_1&wppf_soldlet=show&wppf_orderby=price-desc&wppf_view=list&wppf_lat=0&wppf_lng=0&wppf_radius=10&wppf_records=12"
        self.base_url = "https://www.tayletting.co.uk"
        self.re1 = 'itemtype="http:\/\/schema\.org\/Residence".+href="([^"]+)"'

class DJAlexanderScanner(RightMoveScanner):
    def __init__(self):
        super().__init__()
        self.url = "https://www.djalexander.co.uk/property/to-rent/in-edinburgh/1-and-more-bedrooms/below-1000/"
        self.base_url = "https://djalexander.co.uk"
        self.re1 = '<a href="https:\/\/djalexander\.co\.uk([^"]+)" aria-label'