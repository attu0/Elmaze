import gerber_generator as gg 

# Ask user for folder name
folder_name = input("Enter the name of the folder to generate the Gerber files in: ").strip()

if not folder_name:
    print("❌ Folder name cannot be empty!")
    exit()

PCB_WIDTH = input("Enter the PCB width in inches (e.g., 4): ").strip()
PCB_HEIGHT = input("Enter the PCB height in inches (e.g., 5): ").strip()

component_positions = {
    "Power Supply": (1, 1),
    "Resistor": (3, 1),
    "LED": (3, 3)
}

# Extract pad positions from components
pads = [(x, y) for _, (x, y) in component_positions.items()]

# Define Traces (Connections Between Components)
connections = [
    ("Power Supply", "Resistor"),
    ("Resistor", "LED"),
    ("LED", "Power Supply")
]

traces = [(component_positions[start], component_positions[end]) for start, end in connections]

# Extract Drill Hole Positions (Each component has pins)
holes = [(x, y) for _, (x, y) in component_positions.items()]

# Define Silkscreen Labels (Names at each component location)
silkscreen_positions = [(x + 0.2, y + 0.2) for _, (x, y) in component_positions.items()]

# --- Call Gerber Generation Functions ---
gg.generate_top_layer(pads, traces, folder_name)
gg.generate_board_outline(PCB_WIDTH, PCB_HEIGHT, folder_name)
gg.generate_drill_file(holes, folder_name)
gg.generate_silkscreen(silkscreen_positions, folder_name)

print(f"\n✅ All Gerber files successfully generated in folder: {folder_name}/")
