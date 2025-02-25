import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageOps
import numpy as np
import random

# Load the data from the CSV file
df = pd.read_csv('24hour.csv')

# Filter data to only include "Day 1"
df = df[df['Day'] == 'Day 1']

# Convert the 'Start time' and 'End time' columns to datetime
df['Start time'] = pd.to_datetime(df['Start time'], format='%m/%d/%Y %I:%M:%S%p', errors='coerce')
df['end time'] = pd.to_datetime(df['end time'], format='%m/%d/%Y %I:%M:%S%p', errors='coerce')

# Define colors for different activity types
activity_colors = {
    "sleep": (0, 0, 255, 255),         # Blue
    "relaxing": (0, 255, 0, 255),      # Green
    "travel": (255, 255, 0, 255),      # Yellow
    "physical-fun": (255, 0, 0, 255),  # Red
    "mental-fun": (128, 0, 128, 255),  # Purple
    "eating": (255, 165, 0, 255),      # Orange
    "gaming": (0, 255, 255, 255)       # Cyan
}

# Function to generate a more randomized twirling path
def generate_twirling_path(num_points, radius):
    theta = np.linspace(0, 8 * np.pi, num_points)  # Twisting pattern
    x = np.linspace(-15, 15, num_points) + np.random.uniform(-5, 5, num_points)  # Add randomness
    y = radius * np.sin(theta) + np.random.uniform(-3, 3, num_points)  # Add swirl randomness
    return x, y

# Function to create a star-shaped icon
def create_star(color, size=60):
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))  # Transparent background
    draw = ImageDraw.Draw(img)
    
    points = [
        (size * 0.5, 0), (size * 0.6, size * 0.35), (size, size * 0.35),
        (size * 0.7, size * 0.6), (size * 0.8, size), (size * 0.5, size * 0.75),
        (size * 0.2, size), (size * 0.3, size * 0.6), (0, size * 0.35), (size * 0.4, size * 0.35)
    ]
    draw.polygon(points, fill=color)
    return img

# Function to draw the timeline
def draw_timeline(df, activity_colors):
    fig, ax = plt.subplots(figsize=(24, 36))  # 24x36 inch print size
    ax.set_xlim(-25, 25)
    ax.set_ylim(-45, 45)
    ax.axis('off')
    fig.patch.set_facecolor('#00008B')

    # Generate a randomized swirling path
    x, y = generate_twirling_path(len(df), 20)

    # Add the magic wand at the start
    magic_wand = Image.open("icons/magicwand.png")
    ax.imshow(magic_wand, extent=[x[0] - 2, x[0] + 2, y[0] - 2, y[0] + 2], aspect='auto')

    for index, row in df.iterrows():
        start_time = row['Start time']
        end_time = row['end time']
        activity_type = row['Activity Type'].split(', ')[0]
        color = activity_colors.get(activity_type, (255, 255, 255, 255))

        star_icon = create_star(color, size=60)
        ax.imshow(star_icon, extent=[x[index] - 3, x[index] + 3, y[index] - 3, y[index] + 3], aspect='auto', zorder=2)
        ax.text(x[index], y[index], row['Activity Description'], ha='center', va='center', fontsize=18, color="white")
        ax.text(x[index], y[index] + 1.5, f"{start_time.strftime('%I:%M %p')} - {end_time.strftime('%I:%M %p')}", ha='center', va='top', fontsize=12, color='white')

        if index < len(df) - 1:
            num_sparkles = 200
            x_sparkles = np.linspace(x[index], x[index + 1], num_sparkles) + np.random.uniform(-0.5, 0.5, num_sparkles)
            y_sparkles = np.linspace(y[index], y[index + 1], num_sparkles) + np.random.uniform(-0.5, 0.5, num_sparkles)
            sizes = np.random.rand(num_sparkles) * 15
            colors = np.random.rand(num_sparkles)
            ax.scatter(x_sparkles, y_sparkles, s=sizes, c=colors, marker='*', cmap='cividis', alpha=0.9, zorder=1)

    plt.tight_layout()
    fig.savefig('timeline_24x36_300dpi_rgb.png', format='png', dpi=300, bbox_inches='tight')
    plt.close(fig)

    # Convert to CMYK and save as TIFF
    img_rgb = Image.open('timeline_24x36_300dpi_rgb.png')
    img_cmyk = img_rgb.convert('CMYK')
    img_cmyk.save('timeline_24x36_300dpi_cmyk.tif', dpi=(300, 300), quality=95)

# Draw the timeline
draw_timeline(df, activity_colors)
