import matplotlib.pyplot as plt

# Define the palettes
caramel_light = {
    "Black": "#3B302C",
    "Red": "#C85A54",
    "Green": "#7C9A62",
    "Yellow": "#D6AA5A",
    "Blue": "#89A5C7",
    "Magenta": "#B58696",
    "Cyan": "#6CA9A6",
    "White": "#F5F0E6",
    "Bright Black": "#6D5E55",
    "Bright Red": "#D3756D",
    "Bright Green": "#98B27D",
    "Bright Yellow": "#E2BC76",
    "Bright Blue": "#A3BDD3",
    "Bright Magenta": "#C79DA6",
    "Bright Cyan": "#8ABBB8",
    "Bright White": "#FFFFFF"
}

caramel_dark = {
    "Black": "#2B1B17",
    "Red": "#C06D57",
    "Green": "#9AA86C",
    "Yellow": "#D6A259",
    "Blue": "#7998A9",
    "Magenta": "#AB6B76",
    "Cyan": "#5C9B9A",
    "White": "#D4C7BD",
    "Bright Black": "#5E4B42",
    "Bright Red": "#CF846D",
    "Bright Green": "#AEB87E",
    "Bright Yellow": "#E6B97D",
    "Bright Blue": "#9FB4C2",
    "Bright Magenta": "#BC8994",
    "Bright Cyan": "#76ADA9",
    "Bright White": "#E9DED3"
}

# Function to generate a stacked palette image
def generate_stacked_palette(light_palette, dark_palette, filename):
    fig, ax = plt.subplots(figsize=(16, 6))  # Adjust size for titles and rows
    ax.axis('off')

    # Titles for each row (placed outside plotting region)
    fig.text(0.5, 0.8, "Caramel Light Palette", ha="center", va="center", fontsize=16, weight="bold", color="black", fontfamily="Arial")
    fig.text(0.5, 0.47, "Caramel Dark Palette", ha="center", va="center", fontsize=16, weight="bold", color="black", fontfamily="Arial")

    # Draw the light palette (top row)
    for i, (name, color) in enumerate(light_palette.items()):
        x = i  # Position along the horizontal axis
        display_name = name.replace("Bright ", "Bright\n") if "Bright" in name else name
        ax.add_patch(plt.Rectangle((x, 1.5), 1, 1, color=color, ec="white", lw=2))  # Add white border
        ax.text(
            x + 0.5, 2.1,
            display_name,
            ha="center", va="center",
            fontsize=8, weight="bold",
            color="white" if color in ["#3B302C", "#6D5E55"] else "black",
            fontfamily="Arial"
        )
        ax.text(
            x + 0.5, 1.9,
            f"{color}",
            ha="center", va="center",
            fontsize=8, weight="bold",
            color="white" if color in ["#3B302C", "#6D5E55"] else "black",
            fontfamily="Arial"
        )

    # Draw the dark palette (bottom row)
    for i, (name, color) in enumerate(dark_palette.items()):
        x = i  # Position along the horizontal axis
        display_name = name.replace("Bright ", "Bright\n") if "Bright" in name else name
        ax.add_patch(plt.Rectangle((x, 0), 1, 1, color=color, ec="white", lw=2))  # Add white border
        ax.text(
            x + 0.5, 0.6,
            display_name,
            ha="center", va="center",
            fontsize=8, weight="bold",
            color="white" if color in ["#2B1B17", "#5E4B42"] else "black",
            fontfamily="Arial"
        )
        ax.text(
            x + 0.5, 0.4,
            f"{color}",
            ha="center", va="center",
            fontsize=8, weight="bold",
            color="white" if color in ["#2B1B17", "#5E4B42"] else "black",
            fontfamily="Arial"
        )

    ax.set_xlim(0, 16)  # Ensure 16 slots horizontally
    ax.set_ylim(-0.5, 3)  # Adjust height to ensure spacing
    plt.savefig(f"../palette/{filename}", bbox_inches="tight", dpi=300)
    plt.close()

# Generate the stacked palette image
generate_stacked_palette(caramel_light, caramel_dark, "stacked-palettes.png")
