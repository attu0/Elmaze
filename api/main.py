from pathlib import Path
from . import gerber_generator as gg
from .auto_placer import auto_place_components
from .footprints import generate_all_pads, generate_pad_map

# =========================
# CONFIG
# =========================
COMPONENTS = [
    "Power Supply",
    "Resistor",
    "LED",
]

PIN_CONNECTIONS = [
    (("Power Supply", 0), ("Resistor", 0)),
    (("Resistor", 1), ("LED", 0)),
    (("LED", 1), ("Power Supply", 1)),
]

# =========================
# HELPERS
# =========================
def validate_connections(components, pin_connections):
    for (comp1, _), (comp2, _) in pin_connections:
        if comp1 not in components:
            raise ValueError(f"Invalid component: {comp1}")
        if comp2 not in components:
            raise ValueError(f"Invalid component: {comp2}")


def generate_traces_from_pins(pad_map, pin_connections):
    traces = []

    for ((comp1, pad1), (comp2, pad2)) in pin_connections:
        start = pad_map[comp1][pad1]
        end = pad_map[comp2][pad2]

        # simple L-shape routing
        traces.append((start, (end[0], start[1])))
        traces.append(((end[0], start[1]), end))

    return traces


def generate_silkscreen(component_positions):
    return [(x + 0.2, y + 0.2) for x, y in component_positions.values()]

# =========================
# MAIN FUNCTION (USED BY FASTAPI)
# =========================
def generate_pcb_from_params(output_path: Path, width: float, height: float):
    component_positions = auto_place_components(COMPONENTS, width, height)

    validate_connections(component_positions, PIN_CONNECTIONS)

    pad_map = generate_pad_map(component_positions)
    pads = generate_all_pads(component_positions)
    holes = pads

    traces = generate_traces_from_pins(pad_map, PIN_CONNECTIONS)
    silkscreen = generate_silkscreen(component_positions)

    gg.generate_top_layer(pads, traces, output_path)
    gg.generate_board_outline(width, height, output_path)
    gg.generate_drill_file(holes, output_path)
    gg.generate_silkscreen(silkscreen, output_path)