import math
import random
from typing import Any

from plusminus import ArithmeticParser  # type: ignore[attr-defined]


class ExamMakerParser(ArithmeticParser):  # type: ignore[misc, no-any-unimported]
    def customize(self) -> None:
        super().customize()

        def choose(*values: Any) -> Any:
            return random.choice(values)  # noqa: S311

        def select(i: int, *values: Any) -> Any:
            return values[i]

        def sqrt(value: float) -> float:  # real signature unknown
            return math.sqrt(value)

        self.add_function("choose", ..., choose)
        self.add_function("select", ..., select)
        self.add_function("sqrt", 1, sqrt)
