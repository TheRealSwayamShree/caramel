import matplotlib.pyplot as plt
from caramel_colors import caramel_light, caramel_dark  # Import the light and dark palettes

# Update default font settings
plt.rcParams["font.family"] = "DejaVu Sans"  # Change font to DejaVu Sans

# Function to generate the light palette grid
def generate_light_palette_grid(title, filename):
    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(12, 3.5))  # Adjusted figure size for better aspect ratio
    fig.patch.set_facecolor(caramel_light["White"])  # Set background color to "White"
    ax.axis('off')  # Turn off axes

    # Add title using plt.title
    plt.title(title, fontsize=16, weight="bold", color=caramel_light["Black"], pad=8)

    # Define box size for each color block
    box_size = 1.0

    # Draw the light palette as an 8x2 grid
    for i, (name, color) in enumerate(caramel_light.items()):
        x = i % 8  # Column index
        y = 1 - (i // 8)  # Row index

        # Split "Bright" names into two lines for better readability
        if "Bright" in name:
            display_name = name.replace("Bright ", "Bright\n")
        else:
            display_name = name

        # Combine the name and hex code into a single string
        display_text = f"{display_name}\n{color}"

        # Draw the color block as a rectangle
        ax.add_patch(plt.Rectangle((x, y), box_size, box_size, color=color, ec=caramel_dark["Bright Black"], lw=2))  # Add white border

        # Add the text centered in the block
        ax.text(
            x + box_size / 2, y + box_size / 2,  # Center the text in the block
            display_text,
            ha="center", va="center",  # Center text both horizontally and vertically
            fontsize=10, weight="bold",
            color=caramel_light["White"] if color in ["#3B302C", "#6D5E55"] else caramel_light["Black"]  # Dynamic text color for contrast
        )

    # Set axis limits and aspect ratio
    ax.set_xlim(-0.05, 8.05)  # Small padding to include the grid border
    ax.set_ylim(-0.15, 2.15)  # Small padding to include the grid border
    ax.set_aspect('equal')  # Ensure boxes are square

    # Ensure the bounding box is the same thickness as the grid borders
    ax.spines['top'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    ax.spines['right'].set_linewidth(2)
    ax.spines['top'].set_color(caramel_dark["Bright Black"])
    ax.spines['bottom'].set_color(caramel_dark["Bright Black"])
    ax.spines['left'].set_color(caramel_dark["Bright Black"])
    ax.spines['right'].set_color(caramel_dark["Bright Black"])

    # Save the figure with tight bounding box
    plt.savefig(f"../palette/{filename}", bbox_inches="tight", dpi=300, facecolor=fig.get_facecolor())
    plt.close()

# Function to generate the dark palette grid
def generate_dark_palette_grid(title, filename):
    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(12, 3.5))  # Adjusted figure size for better aspect ratio
    fig.patch.set_facecolor(caramel_dark["Black"])  # Set background color to "Bright Black"
    ax.axis('off')  # Turn off axes

    # Add title using plt.title
    plt.title(title, fontsize=16, weight="bold", color=caramel_dark["White"], pad=8)  # White title for contrast

    # Define box size for each color block
    box_size = 1.0

    # Draw the dark palette as an 8x2 grid
    for i, (name, color) in enumerate(caramel_dark.items()):
        x = i % 8  # Column index
        y = 1 - (i // 8)  # Row index

        # Split "Bright" names into two lines for better readability
        if "Bright" in name:
            display_name = name.replace("Bright ", "Bright\n")
        else:
            display_name = name

        # Combine the name and hex code into a single string
        display_text = f"{display_name}\n{color}"

        # Draw the color block as a rectangle
        ax.add_patch(plt.Rectangle((x, y), box_size, box_size, color=color, ec=caramel_light["White"], lw=2))  # Add white border

        # Add the text centered in the block
        ax.text(
            x + box_size / 2, y + box_size / 2,  # Center the text in the block
            display_text,
            ha="center", va="center",  # Center text both horizontally and vertically
            fontsize=10, weight="bold",
            color=caramel_dark["White"] if color in ["#353232", "#5E4B42"] else caramel_dark["Black"]  # Dynamic text color for contrast
        )

    # Set axis limits and aspect ratio
    ax.set_xlim(-0.05, 8.05)  # Small padding to include the grid border
    ax.set_ylim(-0.15, 2.15)  # Small padding to include the grid border
    ax.set_aspect('equal')  # Ensure boxes are square

    # Ensure the bounding box is the same thickness as the grid borders
    ax.spines['top'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    ax.spines['right'].set_linewidth(2)
    ax.spines['top'].set_color(caramel_light["White"])
    ax.spines['bottom'].set_color(caramel_light["White"])
    ax.spines['left'].set_color(caramel_light["White"])
    ax.spines['right'].set_color(caramel_light["White"])

    # Save the figure with tight bounding box
    plt.savefig(f"../palette/{filename}", bbox_inches="tight", dpi=300, facecolor=fig.get_facecolor())
    plt.close()

# Generate the light and dark palette grids
generate_light_palette_grid("Caramel Light Palette", filename="caramel_light_grid.png")
generate_dark_palette_grid("Caramel Dark Palette", filename="caramel_dark_grid.png")
