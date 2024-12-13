import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from caramel_colors import caramel_light, caramel_dark  # Import palettes from caramel_colors.py
from matplotlib.colors import LinearSegmentedColormap

def hex_to_rgb(hex_color):
    """Convert a hex color to an RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))

def relative_luminance(rgb):
    """Calculate the relative luminance of an RGB color."""
    r, g, b = rgb
    def adjust(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = adjust(r), adjust(g), adjust(b)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast_ratio(color1, color2):
    """Calculate the contrast ratio between two colors."""
    lum1 = relative_luminance(color1)
    lum2 = relative_luminance(color2)
    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)
    return (lighter + 0.05) / (darker + 0.05)

def generate_contrast_matrix(palette):
    """Generate a 16x16 contrast ratio matrix for a given palette."""
    colors = list(palette.values())
    rgb_colors = [hex_to_rgb(color) for color in colors]
    size = len(rgb_colors)
    contrast_matrix = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            contrast_matrix[i, j] = contrast_ratio(rgb_colors[i], rgb_colors[j])
    return contrast_matrix

def save_contrast_matrix_image(matrix, palette, filename, theme_name, background_color):
    """
    Save an image of the contrast matrix with the specified background color and custom colormap.
    
    Parameters:
        matrix (numpy.ndarray): The contrast ratio matrix.
        palette (dict): The color palette.
        filename (str): Output filename for the image.
        theme_name (str): Name of the theme.
        background_color (str): Background color of the image.
    """
    # Custom colormap for light and dark themes
    if background_color == caramel_light["White"]:
        colormap = LinearSegmentedColormap.from_list(
            "light_theme_cmap",
            [caramel_light["Bright Black"], caramel_light["Bright Blue"], caramel_light["Bright White"]]
        )
    elif background_color == caramel_dark["Black"]:
        colormap = LinearSegmentedColormap.from_list(
            "dark_theme_cmap",
            [caramel_dark["Bright Black"], caramel_dark["Bright Blue"], caramel_dark["Bright White"]]
        )
    else:
        colormap = "viridis"  # Default colormap for other themes

    fig, ax = plt.subplots(figsize=(15, 15))
    fig.patch.set_facecolor(background_color)

    if background_color == caramel_light["White"]:
        # Set bounding box color and thickness for light variant
        for spine in ax.spines.values():
            spine.set_edgecolor(caramel_dark["Bright Black"])
            spine.set_linewidth(2)
    elif background_color == caramel_dark["Black"]:
        # Set bounding box color and thickness for dark variant
        for spine in ax.spines.values():
            spine.set_edgecolor(caramel_light["White"])
            spine.set_linewidth(2)
    
    cax = ax.matshow(matrix, cmap=colormap)
    cbar = fig.colorbar(cax, fraction=0.046, pad=0.04)

    if background_color == caramel_light["White"]:
        cbar.outline.set_edgecolor(caramel_dark["Bright Black"])
        cbar.outline.set_linewidth(2)
    elif background_color == caramel_dark["Black"]:
        cbar.outline.set_edgecolor(caramel_light["White"])
        cbar.outline.set_linewidth(2)

    cbar.ax.set_ylabel("Contrast Ratio", rotation=270, labelpad=30, fontsize=20, color=caramel_light["Black"] if background_color == caramel_light["White"] else caramel_dark["White"])  # Larger font size for the cbar label
    cbar.ax.tick_params(labelsize=16, colors=caramel_light["Black"] if background_color == caramel_light["White"] else caramel_dark["White"])  # Larger font size for the cbar numbers

    ax.set_xticks(range(len(palette)))
    ax.set_yticks(range(len(palette)))
    ax.set_xticklabels(palette.keys(), rotation=45, ha="left", fontsize=16, color=caramel_light["Black"] if background_color == caramel_light["White"] else caramel_dark["White"])  # Larger font size for color names
    ax.set_yticklabels(palette.keys(), fontsize=16, color=caramel_light["Black"] if background_color == caramel_light["White"] else caramel_dark["White"])  # Larger font size for color names

    ax.set_xticks(np.arange(0.5, len(palette), 1), minor=True)
    ax.set_yticks(np.arange(0.5, len(palette), 1), minor=True)
    ax.grid(which="minor", color="white", linestyle="-", linewidth=2)
    ax.tick_params(which="minor", size=0)

    for (i, j), val in np.ndenumerate(matrix):
        text_color = caramel_light["Black"]
        ax.text(j, i, f"{val:.1f}", ha='center', va='center', color=text_color, fontsize=14, weight='bold')  # Larger font size for values

    plt.title(f"Contrast Ratio Matrix - {theme_name}", pad=50, fontsize=24, color=caramel_light["Black"] if background_color == caramel_light["White"] else caramel_dark["White"])  # Larger title font size with theme name
    plt.tight_layout()
    plt.savefig(f"../palette/{filename}", facecolor=fig.get_facecolor())  # Ensure background color is saved
    plt.close()

def extract_contrast_pairs(matrix, labels, thresholds):
    """
    Extract color pairs based on contrast ratio thresholds.

    Parameters:
        matrix (numpy.ndarray): Contrast ratio matrix.
        labels (list): List of color names.
        thresholds (list): Threshold values for categorization.

    Returns:
        dict: Dictionary of contrast pairs grouped by threshold.
    """
    contrast_pairs = {f">= {threshold}:1": [] for threshold in thresholds}
    for i, label1 in enumerate(labels):
        for j, label2 in enumerate(labels):
            if i < j:  # Avoid duplicates and diagonal entries
                value = matrix[i, j]
                for threshold in thresholds:
                    if value >= threshold:
                        contrast_pairs[f">= {threshold}:1"].append((label1, label2, value))
                        break
    return contrast_pairs

def save_contrast_pairs_to_csv(pairs_dict, theme_name):
    """
    Save contrast pairs to CSV files grouped by threshold.

    Parameters:
        pairs_dict (dict): Dictionary of contrast pairs grouped by threshold.
        theme_name (str): Name of the theme variant.
    """
    for threshold, pairs in pairs_dict.items():
        if pairs:
            df = pd.DataFrame(pairs, columns=["Color 1", "Color 2", "Contrast Ratio"])
            filename = f"../color_codes/{theme_name.lower().replace(' ', '_')}_contrast_pairs_{threshold.replace(':', '').replace('>= ', '')}.csv"
            df.to_csv(filename, index=False)

def plot_contrast_pairs(pairs_dict, theme_name):
    """
    Generate bar plots for contrast pairs grouped by threshold.

    Parameters:
        pairs_dict (dict): Dictionary of contrast pairs grouped by threshold.
        theme_name (str): Name of the theme variant.
    """
    for threshold, pairs in pairs_dict.items():
        if pairs:
            df = pd.DataFrame(pairs, columns=["Color 1", "Color 2", "Contrast Ratio"])
            plt.figure(figsize=(12, 8))
            plt.barh(
                [f"{row['Color 1']}\n{row['Color 2']}" for _, row in df.iterrows()],  # Split names into two lines
                df["Contrast Ratio"],
                color="skyblue"
            )
            plt.xlabel("Contrast Ratio", fontsize=16)  # Increased text size for x-axis
            plt.ylabel("Color Pairs", fontsize=16)  # Increased text size for y-axis
            plt.xticks(fontsize=14)  # Increased text size for x-axis numbers
            plt.yticks(fontsize=12)  # Increased text size for y-axis labels
            plt.title(f"Contrast Pairs - {theme_name} (Threshold: {threshold})", fontsize=18)
            plt.tight_layout()
            filename = f"../palette/{theme_name.lower().replace(' ', '_')}_contrast_pairs_plot_{threshold.replace(':', '').replace('>= ', '')}.png"
            plt.savefig(filename)
            plt.close()

# Generate contrast matrices for both palettes
light_contrast_matrix = generate_contrast_matrix(caramel_light)
dark_contrast_matrix = generate_contrast_matrix(caramel_dark)

# Save images of contrast matrices with respective backgrounds
save_contrast_matrix_image(
    light_contrast_matrix, caramel_light, "caramel_light_contrast.png", "Caramel Light", caramel_light["White"]
)
save_contrast_matrix_image(
    dark_contrast_matrix, caramel_dark, "caramel_dark_contrast.png", "Caramel Dark", caramel_dark["Black"]
)

# Extract contrast pairs and save to CSV
thresholds = [7, 4.5, 3.1]
light_pairs = extract_contrast_pairs(light_contrast_matrix, list(caramel_light.keys()), thresholds)
dark_pairs = extract_contrast_pairs(dark_contrast_matrix, list(caramel_dark.keys()), thresholds)

save_contrast_pairs_to_csv(light_pairs, "Caramel Light")
save_contrast_pairs_to_csv(dark_pairs, "Caramel Dark")

# Generate plots for contrast pairs
plot_contrast_pairs(light_pairs, "Caramel Light")
plot_contrast_pairs(dark_pairs, "Caramel Dark")
