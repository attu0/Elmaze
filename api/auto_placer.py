from typing import List, Dict, Tuple

Point = Tuple[float, float]


def auto_place_components(
    components: List[str],
    width: float,
    height: float,
    margin: float = 0.5
) -> Dict[str, Point]:
    """
    Automatically place components within PCB boundaries.

    Args:
        components: list of component names
        width: PCB width (inches)
        height: PCB height (inches)
        margin: spacing from edges

    Returns:
        dict: {component_name: (x, y)}
    """

    if width <= 2 * margin or height <= 2 * margin:
        raise ValueError("Board too small for given margin")

    if not components:
        raise ValueError("Component list cannot be empty")

    usable_width = width - 2 * margin
    usable_height = height - 2 * margin

    n = len(components)
    positions = {}

    # Horizontal distribution (simple + clean)
    step_x = usable_width / max(n - 1, 1)

    for i, comp in enumerate(components):
        x = margin + i * step_x
        y = margin + usable_height / 2  # center vertically

        positions[comp] = (round(x, 3), round(y, 3))

    return positions