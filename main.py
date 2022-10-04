from WebScanner import *
from NotificationService import *
from CacheService import *
from Property import *
import time, sys
from datetime import datetime

class App:
    def __init__(self, refreshRate):
        self.refreshRate = refreshRate
        self.notificationService = ConsoleNotificationService()#EmailNotificationService()
        self.cacheService = CacheService("cache.json")
        self.webScanners = [
            RightMoveScanner(), ZooplaScanner(),
            OnTheMarkerScanner(), S1HomesScanner(),
            TayLettingsScanner(), DJAlexanderScanner()
            ]

        self._initCache()

    def _initCache(self):
        if self.cacheService.get("notifiedProperties") == None:
            self.cacheService.set("notifiedProperties", [])

    def _getNewProperties(self, properties):
        return [x for x in properties if x.id not in self.cacheService.get("notifiedProperties")]

    def _notifyAboutProperties(self, properties):
        notificationText = "New properties:\n"
        for p in properties:
            notificationText += p.url + "\n"
        self.notificationService.notify(notificationText)

    def _updateCachedProperties(self, properties):
        ids = [x.id for x in properties]
        self.cacheService.get("notifiedProperties").extend(ids)

    def _getTimestamp(self):
        return str(datetime.now())

    def run(self):
        while True:
            properties = []
            for s in self.webScanners:
                properties += s.scan()
            newProperties = self._getNewProperties(properties)
            print("App: [{0}] Found {1} new properties.".format(self._getTimestamp(), len(newProperties)))
            if len(newProperties) > 0:
                self._notifyAboutProperties(newProperties)
                self._updateCachedProperties(newProperties)
            time.sleep(self.refreshRate)

print("App: Starting up...")

stop = False
app = App(30)

if len(sys.argv) == 2 and sys.argv[1] == "clear":
    print("App: clearing cache...")
    app.cacheService.clear()
    app.cacheService.save()
    exit()

while not stop:

    try:
        app.run()
    except KeyboardInterrupt as e:
        print("App: Shutting down...")
        stop = True
    except Exception as e:
        print("App: An exception has occured: {0}".format(e))

app.cacheService.save()
