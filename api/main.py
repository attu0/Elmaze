from pathlib import Path
import sys
import gerber_generator as gg


# =========================
# Configuration
# =========================
PCB_WIDTH = 5
PCB_HEIGHT = 5

COMPONENT_POSITIONS = {
    "Power Supply": (1, 1),
    "Resistor": (3, 1),
    "LED": (3, 3),
}

CONNECTIONS = [
    ("Power Supply", "Resistor"),
    ("Resistor", "LED"),
    ("LED", "Power Supply"),
]


# =========================
# Utility Functions
# =========================
def get_output_folder() -> Path:
    """Prompt user for output folder and validate."""
    folder_name = input("Enter output folder name: ").strip()

    if not folder_name:
        raise ValueError("Folder name cannot be empty")

    output_path = Path(folder_name)

    try:
        output_path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise RuntimeError(f"Failed to create folder: {e}")

    return output_path


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
def generate_pcb(output_path: Path):
    """Main PCB generation pipeline."""
    print("🔍 Validating design...")
    validate_connections(COMPONENT_POSITIONS, CONNECTIONS)

    print("📐 Preparing layout data...")
    pads = extract_pads(COMPONENT_POSITIONS)
    traces = extract_traces(COMPONENT_POSITIONS, CONNECTIONS)
    holes = extract_holes(COMPONENT_POSITIONS)
    silkscreen = extract_silkscreen(COMPONENT_POSITIONS)

    print("⚙️ Generating Gerber files...")

    # ✅ FIX: Pass Path object (NOT string)
    gg.generate_top_layer(pads, traces, output_path)
    gg.generate_board_outline(PCB_WIDTH, PCB_HEIGHT, output_path)
    gg.generate_drill_file(holes, output_path)
    gg.generate_silkscreen(silkscreen, output_path)

    print(f"\n✅ Gerber files generated successfully in: {output_path.resolve()}")


def main():
    try:
        output_path = get_output_folder()
        generate_pcb(output_path)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()