from plusminus import ArithmeticParser
import random
import math


class ExamMakerParser(ArithmeticParser):
    def customize(self):
        super().customize()

        def choose(*values):
            return random.choice(values)

        def select(i, *values):
            return values[i]

        def sqrt(value):
            return math.sqrt(value)

        self.add_function("choose", ..., choose)
        self.add_function("select", ..., select)
        self.add_function("sqrt", 1, sqrt)
