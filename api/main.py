from pathlib import Path
import sys
import gerber_generator as gg
from auto_placer import auto_place_components


# =========================
# Configuration
# =========================
BASE_OUTPUT_DIR = Path(r"D:\El-Maze\2026\gerber_files")

COMPONENTS = [
    "Power Supply",
    "Resistor",
    "LED",
]

CONNECTIONS = [
    ("Power Supply", "Resistor"),
    ("Resistor", "LED"),
    ("LED", "Power Supply"),
]


# =========================
# Input Functions
# =========================
def get_board_dimensions():
    """Prompt user for PCB dimensions with validation."""
    try:
        width_input = input("Enter PCB width (in inches): ").strip()
        height_input = input("Enter PCB height (in inches): ").strip()

        width = float(width_input)
        height = float(height_input)

        if width <= 0 or height <= 0:
            raise ValueError("Dimensions must be positive numbers")

        return width, height

    except ValueError as e:
        raise ValueError(f"Invalid input for PCB dimensions: {e}")


def get_output_folder() -> Path:
    """Return fixed Gerber directory with optional project subfolder."""

    project_name = input("Enter project name (optional): ").strip()

    output_path = BASE_OUTPUT_DIR / project_name if project_name else BASE_OUTPUT_DIR

    try:
        output_path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise RuntimeError(f"Failed to create folder: {e}")

    return output_path


# =========================
# Utility Functions
# =========================
def validate_connections(components, connections):
    """Ensure all connections refer to valid components."""
    for start, end in connections:
        if start not in components:
            raise ValueError(f"Invalid component in connection: {start}")
        if end not in components:
            raise ValueError(f"Invalid component in connection: {end}")


def extract_pads(components):
    return list(components.values())


def extract_traces(components, connections):
    return [(components[start], components[end]) for start, end in connections]


def extract_holes(components):
    return list(components.values())


def extract_silkscreen(components):
    return [(x + 0.2, y + 0.2) for x, y in components.values()]


# =========================
# Main Logic
# =========================
def generate_pcb(output_path: Path, width: float, height: float):
    """Main PCB generation pipeline."""

    print("📍 Auto-placing components...")
    component_positions = auto_place_components(COMPONENTS, width, height)

    print("🔍 Validating design...")
    validate_connections(component_positions, CONNECTIONS)

    print("📐 Preparing layout data...")
    pads = extract_pads(component_positions)
    traces = extract_traces(component_positions, CONNECTIONS)
    holes = extract_holes(component_positions)
    silkscreen = extract_silkscreen(component_positions)

    print("⚙️ Generating Gerber files...")

    gg.generate_top_layer(pads, traces, output_path)
    gg.generate_board_outline(width, height, output_path)
    gg.generate_drill_file(holes, output_path)
    gg.generate_silkscreen(silkscreen, output_path)

    print(f"\n✅ Gerber files generated successfully in: {output_path.resolve()}")


# =========================
# Entry Point
# =========================
def main():
    try:
        print("\n🛠 PCB Generator\n")

        output_path = get_output_folder()
        pcb_width, pcb_height = get_board_dimensions()

        generate_pcb(output_path, pcb_width, pcb_height)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()