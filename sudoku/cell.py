from pydantic import BaseModel, Field
from copy import copy


class Cell(BaseModel):
    value: int | None = Field(default=None)
    possible_values: set[int] = Field(default={1, 2, 3, 4, 5, 6, 7, 8, 9})

    def set_value(self, v: int, p: set = set()):
        self.value = v
        if len(p) == 0:
            self.possible_values = {v}
        else:
            self.possible_values = p

    def __eq__(self, other: "Cell"):
        return (
            self.value == other.value and self.possible_values == other.possible_values
        )

    def copy(self):
        return copy(self)
