import os

# Define global PCB settings
PRECISION = "FSLAX24Y24"
UNITS = "MOIN"  # Inches
SCALE_FACTOR = 1000  # Ensures all coordinates match drill file


def write_gerber_file(filename, content, folder_name="gerber_files"):
    """Write content to a Gerber file."""
    os.makedirs(folder_name, exist_ok=True)
    filepath = os.path.join(folder_name, filename)
    with open(filepath, "w") as file:
        file.write(content)
    print(f"Generated: {filename}")


def generate_top_layer(pads, traces, folder_name="gerber_files"):
    """Generate the top copper layer (GTL)."""
    content = f"""G04 Top Copper Layer*
%{PRECISION}*%
%{UNITS}*%
G75*
%ADD10C,0.062*%
%ADD11C,0.030*%
G54D10*
"""
    # Add pads
    for x, y in pads:
        content += f"X{x*SCALE_FACTOR}Y{y*SCALE_FACTOR}D03*\n"

    # Add traces
    content += "G54D11*\nD11*\n"
    for (x1, y1), (x2, y2) in traces:
        content += f"X{x1*SCALE_FACTOR}Y{y1*SCALE_FACTOR}D02*\n"
        content += f"X{x2*SCALE_FACTOR}Y{y2*SCALE_FACTOR}D01*\n"

    content += "M02*\n"
    write_gerber_file("top_layer.gtl", content, folder_name)


def generate_board_outline(width, height, folder_name="gerber_files"):
    """Generate the board outline (GKO)."""
    content = f"""G04 Board Outline*
%{PRECISION}*%
%{UNITS}*%
G75*
%ADD10C,0.020*%
G54D10*
D10*
X0Y0D02*
X{width*SCALE_FACTOR}Y0D01*
X{width*SCALE_FACTOR}Y{height*SCALE_FACTOR}D01*
X0Y{height*SCALE_FACTOR}D01*
X0Y0D01*
M02*
"""
    write_gerber_file("board_outline.gko", content, folder_name)


def generate_drill_file(holes, folder_name="gerber_files"):
    """Generate the drill file (DRL)."""
    content = """M48
INCH,TZ
T1C0.0315
%
T1
"""
    for x, y in holes:
        content += f"X{x*SCALE_FACTOR}Y{y*SCALE_FACTOR}\n"

    content += "M30\n"
    write_gerber_file("drill_through.drl", content, folder_name)


def generate_silkscreen(positions, folder_name="gerber_files"):
    """Generate the silkscreen layer (GTO)."""
    content = f"""G04 Top Silkscreen*
%{PRECISION}*%
%{UNITS}*%
G75*
%ADD12C,0.030*%
G54D12*
D12*
"""
    for x, y in positions:
        content += f"X{x*SCALE_FACTOR}Y{y*SCALE_FACTOR}D02*\n"

    content += "M02*\n"
    write_gerber_file("top_silkscreen.gto", content, folder_name)
