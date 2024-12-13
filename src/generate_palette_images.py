import matplotlib.pyplot as plt
from caramel_colors import caramel_light, caramel_dark  # Import palettes

# Update default font settings
plt.rcParams["font.family"] = "DejaVu Sans"  # Change font to DejaVu Sans

# Function to generate an 8x2 grid palette image
def generate_palette_grid(palette, title, filename):
    fig, ax = plt.subplots(figsize=(12, 3.5))  # Adjusted figure size for better aspect ratio
    ax.axis('off')

    # Add title using plt.title
    plt.title(title, fontsize=16, weight="bold", color="black", pad=8)

    # Define box size
    box_size = 1.0

    # Draw the palette as an 8x2 grid
    for i, (name, color) in enumerate(palette.items()):
        x = i % 8  # Column index
        y = 1 - (i // 8)  # Row index

        # Split "Bright" names into two lines
        if "Bright" in name:
            display_name = name.replace("Bright ", "Bright\n")
        else:
            display_name = name

        # Combine the name and hex code
        display_text = f"{display_name}\n{color}"

        # Draw the color block
        ax.add_patch(plt.Rectangle((x, y), box_size, box_size, color=color, ec="white", lw=2))  # Add white border

        # Add the text centered in the block
        ax.text(
            x + box_size / 2, y + box_size / 2,
            display_text,
            ha="center", va="center",  # Center text both horizontally and vertically
            fontsize=10, weight="bold",
            color="white" if color in ["#3B302C", "#6D5E55", "#2B1B17", "#5E4B42"] else "black"
        )

    # Set axis limits and aspect ratio
    ax.set_xlim(0, 8)
    ax.set_ylim(-0.1, 2)  # Reduced bottom padding further
    ax.set_aspect('equal')  # Ensure boxes are square

    # Save the figure with tight bounding box
    plt.savefig(f"../palette/{filename}", bbox_inches="tight", dpi=300)
    plt.close()

# Generate the 8x2 grids
generate_palette_grid(caramel_light, "Caramel Light Palette", filename="caramel_light_grid.png")
generate_palette_grid(caramel_dark, "Caramel Dark Palette", filename="caramel_dark_grid.png")
