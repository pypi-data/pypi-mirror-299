# jose_market/jose.py

class Jose:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print(f"Olá, {self.name}! Bem-vindo ao JoseMarket.")

    def sum_values(self, a, b):
        return a + b
