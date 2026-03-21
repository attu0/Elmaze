from typing import Dict, List, Tuple

Point = Tuple[float, float]


# =========================
# Footprint Definitions (THT)
# =========================
FOOTPRINTS: Dict[str, List[Point]] = {
    "Resistor": [
        (-0.3, 0.0),
        (0.3, 0.0),
    ],
    "LED": [
        (-0.1, 0.0),
        (0.1, 0.0),
    ],
    "Power Supply": [
        (-0.2, 0.0),
        (0.2, 0.0),
    ],
}


# =========================
# API Functions
# =========================
def get_footprint(component_name: str) -> List[Point]:
    """Return footprint pad offsets for a component."""
    if component_name not in FOOTPRINTS:
        raise ValueError(f"No footprint defined for: {component_name}")

    return FOOTPRINTS[component_name]


def generate_all_pads(component_positions: Dict[str, Point]) -> List[Point]:
    """
    Expand component positions into actual pad positions.
    
    Returns:
        List of absolute pad coordinates
    """
    pads: List[Point] = []

    for comp, (cx, cy) in component_positions.items():
        footprint = get_footprint(comp)

        for dx, dy in footprint:
            pad_x = cx + dx
            pad_y = cy + dy
            pads.append((round(pad_x, 3), round(pad_y, 3)))

    return pads

def generate_pad_map(component_positions):
    """
    Returns:
        {
            "Resistor": [(x1,y1), (x2,y2)],
            "LED": [(x1,y1), (x2,y2)]
        }
    """
    pad_map = {}

    for comp, (cx, cy) in component_positions.items():
        footprint = get_footprint(comp)

        pad_list = []
        for dx, dy in footprint:
            pad_x = round(cx + dx, 3)
            pad_y = round(cy + dy, 3)
            pad_list.append((pad_x, pad_y))

        pad_map[comp] = pad_list

    return pad_map