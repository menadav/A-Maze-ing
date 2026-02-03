import sys

try:
    from pydantic import BaseModel, Field, model_validator
except ImportError:
    sys.stderr.write("Pydantic not found: Install -> pip install pydantic")
    sys.exit(1)


class MazeConfig(BaseModel):
    """Configuration model for maze generation and solving.

    Validates dimensions, entry and exit positions, algorithm selection,
    solver choice, and optional seed values.
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
        """Validate entry and exit coordinates.

        Ensures that:
        - Both coordinates contain exactly two integers.
        - Entry and exit lie within maze bounds.
        - Entry and exit are not the same position.

        Returns:
            The validated configuration instance.

        Raises:
            ValueError: If coordinates are invalid or out of bounds.
        """
        w, h = self.width, self.height
        ex, ey = self.entry
        xx, xy = self.exit_

        if len(self.entry) != 2 or len(self.exit_) != 2:
            raise ValueError(
                "Entry and exit must contain exactly two numbers"
            )

        if not (0 <= ex < w and 0 <= ey < h):
            raise ValueError("Entry must be inside maze bounds")

        if not (0 <= xx < w and 0 <= xy < h):
            raise ValueError("Exit must be inside maze bounds")

        if (ex, ey) == (xx, xy):
            raise ValueError("Entry and exit cannot be in the same position")

        return self
