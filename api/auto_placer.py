from typing import List, Dict, Tuple
import math

Point = Tuple[float, float]


def auto_place_components(
    components: List[str],
    width: float,
    height: float,
    margin: float = 0.5
) -> Dict[str, Point]:

    if width <= 2 * margin or height <= 2 * margin:
        raise ValueError("Board too small for given margin")

    if not components:
        raise ValueError("Component list cannot be empty")

    usable_width = width - 2 * margin
    usable_height = height - 2 * margin

    n = len(components)

    positions = {}

    # Create grid (2 rows)
    rows = 2
    cols = math.ceil(n / rows)

    step_x = usable_width / max(cols - 1, 1)
    step_y = usable_height / max(rows - 1, 1)

    for i, comp in enumerate(components):
        row = i % rows
        col = i // rows

        x = margin + col * step_x
        y = margin + row * step_y

        positions[comp] = (round(x, 3), round(y, 3))

    return positions