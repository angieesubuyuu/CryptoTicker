class CryptoOption:
    def __init__(self, name, symbol, price):
        self.name = name
        self.symbol = symbol
        self.price = price

    def __str__(self):
        return f"{self.name} (${self.price})"
    
    def get_formatted_price(self):
        return f"{self.price:,.2f}"