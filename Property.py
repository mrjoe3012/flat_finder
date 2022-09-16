# holds data about a property
class Property:
    def __init__(self, id, url):
        self.id = id
        self.url = url

    def __str__(self):
        return "id: {0}, url: {1}".format(self.id, self.url)