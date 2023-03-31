class ClickHousePrinter:
    def __init__(self, ast):
        self.ast = ast

    def print(self):
        return str(self.ast)
