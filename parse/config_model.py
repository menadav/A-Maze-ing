import sys

try:
    from pydantic import BaseModel, Field, model_validator, ValidationError
except ImportError:
    sys.stderr.write("Pydantic not found: Install -> pip install pydantic")
    sys.exit(1)


class MazeConfig(BaseModel):
    """
    Typed configuration model for maze generation and solving.
    Validates dimensions, entry/exit positions, algorithm, and solver.
    """
    width: int = Field(ge=2)
    height: int = Field(ge=2)
    entry: tuple[int, int]
    exit_: tuple[int, int] = Field(alias="exit")
    output_file: str
    seed: int | None = None
    perfect: bool = True
    algorithm: str = "prim"
    solver: str = "bfs"

    @model_validator(mode="after")
    def validations(self) -> "MazeConfig":
        """
        Validate entry/exit coordinates and ensure they 
        lie within bounds and are not identical.
        """
        w, h = self.width, self.height
        ex, ey = self.entry
        xx, xy = self.exit_
        if len(self.entry) != 2 or len(self.exit_) != 2:
            raise ValidationError(
                "Entry and exit must be composted of exactly 2 numbers"
            )
        if not (0 <= ex < w and 0 <= ey < h):
            raise ValueError("Entry must be inside maze bounds")
        if not (0 <= xx < w and 0 <= xy < h):
            raise ValueError("Exit must be inside maze bounds")
        if (ex, ey) == (xx, xy):
            raise ValueError("Entry and exit cannot be in same spot")

        return self
