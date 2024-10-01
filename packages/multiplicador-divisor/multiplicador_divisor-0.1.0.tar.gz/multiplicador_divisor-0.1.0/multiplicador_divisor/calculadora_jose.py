class CalculadoraJose:
    def multiplica(self, a, b):
        """Retorna o produto de a e b."""
        return a * b

    def divide(self, a, b):
        """Retorna a divisão de a por b. Lança um erro se b for zero."""
        if b == 0:
            raise ValueError("Não é possível dividir por zero.")
        return a / b
