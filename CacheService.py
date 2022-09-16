import json

# provides a pesistent cache
class CacheService:
    def __init__(self, filename):
        self._cache = {}
        self._filename = filename
        self._load(filename)

    # loads the cache data from a json file
    def _load(self, filename):
        print("CacheService: Loading cache from '{0}'".format(filename))
        try:
            with open(filename, "r") as file:
                data = file.read()
                self._cache = json.loads(data)
        except FileNotFoundError as e:
            print("CacheService: Unable to locate '{0}', creating an empty cache.".format(filename))
            self._cache = {}
        except:
            raise Exception("CacheService: Failed to load cache.")
        print("CacheService: Successfully loaded cache with {0} entries.".format(len(self._cache)))

    # saves the data in the cache to the disc
    def save(self):
        print("CacheService: Saving cache to '{0}'".format(self._filename))
        try:
            with open(self._filename, "w") as file:
                file.write(json.dumps(self._cache))
        except:
            raise Exception("CacheService: Failed to save cache.")
        print("CacheService: Successfuly saved cache with {0} entries.".format(len(self._cache)))

    def clear(self):
        print("CacheService: Clearing cache.")
        self._cache = {}

    def get(self, key):
        return self._cache.get(key, None)

    def set(self, key, value):
        self._cache[key] = value