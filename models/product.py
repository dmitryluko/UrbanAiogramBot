class Product:
    def __init__(self, title, price, description=None, pic_ref=None):
        self.title = title
        self.description = description
        self.price = price
        self.img_ref = pic_ref
