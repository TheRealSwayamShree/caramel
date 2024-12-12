# Caramel Theme Colors

# Define the color palettes for Caramel Light and Caramel Dark
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

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

def save_contrast_matrix_image(matrix, palette, filename, theme_name):
    """Save an image of the contrast matrix with white grid lines excluding the edges of the matrix."""
    fig, ax = plt.subplots(figsize=(15, 15))  # Further increased image size
    cax = ax.matshow(matrix, cmap="viridis")
    cbar = fig.colorbar(cax, fraction=0.046, pad=0.04)
    cbar.ax.set_ylabel("Contrast Ratio", rotation=270, labelpad=30, fontsize=20)  # Larger font size for the cbar label
    cbar.ax.tick_params(labelsize=16)  # Larger font size for the cbar numbers

    ax.set_xticks(range(len(palette)))
    ax.set_yticks(range(len(palette)))
    ax.set_xticklabels(palette.keys(), rotation=45, ha="left", fontsize=16)  # Larger font size for color names
    ax.set_yticklabels(palette.keys(), fontsize=16)  # Larger font size for color names

    ax.set_xticks(np.arange(0.5, len(palette), 1), minor=True)
    ax.set_yticks(np.arange(0.5, len(palette), 1), minor=True)
    ax.grid(which="minor", color="white", linestyle="-", linewidth=2)
    ax.tick_params(which="minor", size=0)

    for (i, j), val in np.ndenumerate(matrix):
        ax.text(j, i, f"{val:.1f}", ha='center', va='center', color="white", fontsize=14)  # Larger font size for values

    plt.title(f"Contrast Ratio Matrix - {theme_name}", pad=50, fontsize=24)  # Larger title font size with theme name
    plt.tight_layout()
    plt.savefig(f"../palette/{filename}")
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

# Save images of contrast matrices
save_contrast_matrix_image(light_contrast_matrix, caramel_light, "caramel_light_contrast.png", "Caramel Light")
save_contrast_matrix_image(dark_contrast_matrix, caramel_dark, "caramel_dark_contrast.png", "Caramel Dark")

# Extract contrast pairs and save to CSV
thresholds = [7, 4.5, 3.1]
light_pairs = extract_contrast_pairs(light_contrast_matrix, list(caramel_light.keys()), thresholds)
dark_pairs = extract_contrast_pairs(dark_contrast_matrix, list(caramel_dark.keys()), thresholds)

save_contrast_pairs_to_csv(light_pairs, "Caramel Light")
save_contrast_pairs_to_csv(dark_pairs, "Caramel Dark")

# Generate plots for contrast pairs
plot_contrast_pairs(light_pairs, "Caramel Light")
plot_contrast_pairs(dark_pairs, "Caramel Dark")
