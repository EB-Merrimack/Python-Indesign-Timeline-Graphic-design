import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse  # Correct import for Ellipse
from PIL import Image, ImageDraw
import numpy as np

# Load the data from the CSV file
df = pd.read_csv('24hour.csv')

# Filter data to only include "Day 1"
df = df[df['Day'] == 'Day 1']

# Convert the 'Start time' and 'End time' columns to datetime
df['Start time'] = pd.to_datetime(df['Start time'], format='%m/%d/%Y %I:%M:%S%p', errors='coerce')
df['End time'] = pd.to_datetime(df['end time'], format='%m/%d/%Y %I:%M:%S%p', errors='coerce')

# Define updated colors for different activity types with alpha transparency
activity_colors = {
    "sleep": (0, 0, 255, 128),         # Blue with 50% transparency
    "relaxing": (0, 255, 0, 200),      # Green with 80% transparency
    "travel": (255, 255, 0, 255),      # Yellow with full opacity
    "physical-fun": (255, 0, 0, 255),  # Red with full opacity
    "mental-fun": (128, 0, 128, 180),  # Purple with 70% transparency
    "eating": (255, 165, 0, 200),      # Orange with 80% transparency
    "gaming": (0, 255, 255, 150)       # Cyan with 60% transparency
}

# Function to generate a spiral path with more space between the points
def generate_spiral_path(num_points, radius):
    theta = np.linspace(0, 8 * np.pi, num_points)  # More rotations for a larger spiral
    r = np.linspace(0, radius, num_points)  # Radial distance increases
    x = r * np.cos(theta)  # X coordinate
    y = r * np.sin(theta)  # Y coordinate
    return x, y

# Function to create a solid mini star icon (same size as the sparkles)
def create_mini_star(color, size=3):  # Adjusted size to be smaller
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))  # Smaller size
    draw = ImageDraw.Draw(img)
    
    # Star shape coordinates (adjusted for smaller size)
    points = [
        (size * 0.5, 0), (size * 0.6, size * 0.35), (size, size * 0.35),
        (size * 0.7, size * 0.6), (size * 0.8, size), (size * 0.5, size * 0.75),
        (size * 0.2, size), (size * 0.3, size * 0.6), (0, size * 0.35), (size * 0.4, size * 0.35)
    ]
    
    # Draw the star with the given color
    draw.polygon(points, fill=color)
    return img

# Function to generate shades of a color by modifying brightness and alpha in a smooth way
def generate_shades(base_color, num_shades=5):
    shades = []
    r, g, b, a = base_color
    # Create smooth variations in brightness and opacity
    for i in range(num_shades):
        # Evenly adjust brightness by scaling the RGB values in a gradient-like way
        factor = 1 + (i / (num_shades - 1)) * 0.4  # Gradual change, more spread-out variations
        new_r = int(min(255, r * factor))
        new_g = int(min(255, g * factor))
        new_b = int(min(255, b * factor))
        new_a = int(min(255, a + (np.sin(i * np.pi / (num_shades - 1)) * 40)))  # Smooth alpha variation
        shades.append((new_r, new_g, new_b, new_a))
    return shades

# Function to draw the timeline
def draw_timeline(df, activity_colors):
    fig, ax = plt.subplots(figsize=(24, 36))
    ax.set_xlim(-30, 30)
    ax.set_ylim(-50, 50)
    ax.axis('off')
    fig.patch.set_facecolor('#00008B')

    # Generate a larger spiral path
    x, y = generate_spiral_path(len(df), 30)

    # Add the magic wand at the start (optional, replace the path if you don't want it)
    try:
        magic_wand = Image.open("icons/magicwand.png")
        rotated_wand = magic_wand.rotate(45, expand=True)
        ax.imshow(rotated_wand, extent=[x[0] - 1.5, x[0] + 1.5, y[0] - 1.5, y[0] + 1.5], aspect='auto')
    except FileNotFoundError:
        print("Magic wand image not found!")

    for index, row in df.iterrows():
        start_time, end_time = row['Start time'], row['End time']
        activity_type = row['Activity Type'].split(', ')[0]
        base_color = activity_colors.get(activity_type, (255, 255, 255, 255))

        # Generate multiple shades of the activity color for the burst effect
        shades = generate_shades(base_color, num_shades=7)
        
        # Draw mini stars along the spiral outline with different shades
        num_mini_stars = 12  # Number of mini stars around the outline
        angle = np.linspace(0, 2 * np.pi, num_mini_stars, endpoint=False)  # Full circle
        burst_radius = 3  # Radius of the burst, adjusted for smaller size
        for i in range(num_mini_stars):
            x_pos = x[index] + burst_radius * np.cos(angle[i])
            y_pos = y[index] + burst_radius * np.sin(angle[i])
            # Alternate between different shades
            shade = shades[i % len(shades)]
            mini_star_icon = create_mini_star(shade, size=3)  # Smaller burst stars to match sparkle size
            ax.imshow(mini_star_icon, extent=[x_pos - 1.5, x_pos + 1.5, y_pos - 1.5, y_pos + 1.5], aspect='auto')

        # Add shadow for the activity info (text and icon)
        ax.text(x[index], y[index] + 1.5, row['Activity Description'], ha='center', va='center', fontsize=18, 
                color='black', alpha=0.7, fontweight='bold', zorder=2)  # Shadow
        ax.text(x[index], y[index] + 1.5, row['Activity Description'], ha='center', va='center', fontsize=18, 
                color='white', fontweight='bold', zorder=3)  # Main text
        
        ax.text(x[index], y[index] + 3, f"{start_time.strftime('%I:%M %p')} - {end_time.strftime('%I:%M %p')}", 
                ha='center', va='top', fontsize=12, color='black', alpha=0.7, zorder=2)  # Shadow
        ax.text(x[index], y[index] + 3, f"{start_time.strftime('%I:%M %p')} - {end_time.strftime('%I:%M %p')}", 
                ha='center', va='top', fontsize=12, color='white', zorder=3)  # Main time

        # Add sparkle trail between activities
        if index < len(df) - 1:
            num_sparkles = 200
            x_sparkles = np.linspace(x[index], x[index + 1], num_sparkles)
            y_sparkles = np.linspace(y[index], y[index + 1], num_sparkles)
            x_sparkles += np.random.uniform(-0.3, 0.3, size=num_sparkles)
            y_sparkles += np.random.uniform(-0.3, 0.3, size=num_sparkles)
            sizes = np.random.rand(num_sparkles) * 5  # Match sparkle size
            colors = np.random.rand(num_sparkles)
            ax.scatter(x_sparkles, y_sparkles, s=sizes, c=colors, marker='*', cmap='cividis', alpha=0.9, zorder=1)

        # Add shadow underneath the oval (using a darker shade of the activity color)
        shadow_color = tuple([c * 0.5 / 255 for c in base_color[:3]]) + (0.588,)  # 150/255 = 0.588
        ax.add_patch(Ellipse((x[index], y[index]), width=12, height=8, color=shadow_color, alpha=0.5))

    plt.tight_layout()
    plt.show()

# Draw the timeline
draw_timeline(df, activity_colors)
