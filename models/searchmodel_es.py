class PropertySearch:
    def __init__(self, title, amenities, price, location):
        self.title = title
        self.amenities = amenities
        self.price = price
        self.location = location

    def to_dict(self):
        return {
            "title": self.title,
            "amenities": self.amenities,
            "price": self.price,
            "location": self.location
        }
