

class SimpleCalculator:
    def __init__(self):
        self.result = 0

    def add(self, left: float, right: float) -> float:
        self.result = left + right
        return self.result
    
    def sub(self, left: float, right: float) -> float:
        self.result = left - right
        return self.result

    def mul(self, left: float, right: float) -> float:
        self.result = left * right
        return self.result

    def div(self, left: float, right: float) -> float:
        self.result = left / right
        return self.result
    
    def mod(self, left: float, right: float) -> float:
        self.result = left % right
        return self.result
    
    def floor(self, left: float, right: float) -> int:
        self.result = left // right
        return self.result
    
    def equal(self, left: float, right: float) -> float:
        self.result = (left == right)
        return self.result 
    
    def get_result(self):
        return self.result
    
