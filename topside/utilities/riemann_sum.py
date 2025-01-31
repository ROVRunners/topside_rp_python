
class Riemann:
    """a callable class the performs a riemann sum on the accumulated data given"""

    _conversion_factor: float
    graph: list[list[float,float]]

    def __init__(self, conversion_factor: float):
        self._conversion_factor = conversion_factor
        self.graph = []

    def __call__(self, y_val, x_val):
        self.graph += [y_val, x_val]
        return self.left_handed_summation() * self._conversion_factor


    def left_handed_summation(self):
        total_sum = 0
        for i in range(len(self.graph)):
            total_sum += self.graph[i][1]
        return total_sum * len(self.graph)

