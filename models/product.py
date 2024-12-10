class Product:
    def __init__(self, title, price, description=None, img_ref=None, _id=None):
        self._id = _id
        self.title = title
        self.description = description
        self.price = price
        self.img_ref = img_ref
