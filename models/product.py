class Product:
    def __init__(self, id, title, description, price):
        self.id = id
        self.title = title
        self.description = description
        self.price = price

    # @staticmethod
    # def from_sql_row(row):
    #     return Product(row[0], row[1], row[2], row[3])
