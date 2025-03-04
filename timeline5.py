import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import numpy as np

# Load the data from the CSV file
df = pd.read_csv('24hour.csv')

# Filter data to only include "Day 1"
df = df[df['Day'] == 'Day 1']

# Convert the 'Start time' and 'End time' columns to datetime
df['Start time'] = pd.to_datetime(df['Start time'], format='%m/%d/%Y %I:%M:%S%p', errors='coerce')
df['End time'] = pd.to_datetime(df['end time'], format='%m/%d/%Y %I:%M:%S%p', errors='coerce')

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

# Function to generate a spiral path with more space between the points
def generate_spiral_path(num_points, radius):
    theta = np.linspace(0, 6 * np.pi, num_points)  # More rotations for a larger spiral
    r = np.linspace(0, radius, num_points)  # Radial distance increases
    x = r * np.cos(theta)  # X coordinate
    y = r * np.sin(theta)  # Y coordinate
    return x, y

# Function to create a mini star icon
def create_mini_star(color, size=10):
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
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
        color = activity_colors.get(activity_type, (255, 255, 255, 255))
        
        # Draw mini stars along the spiral outline
        mini_star_icon = create_mini_star(color, size=12)
        num_mini_stars = 12  # Number of mini stars around the outline
        angle = np.linspace(0, 2 * np.pi, num_mini_stars, endpoint=False)  # Full circle
        for i in range(num_mini_stars):
            # Create circular positions for mini stars around the main position
            x_pos = x[index] + 2 * np.cos(angle[i])
            y_pos = y[index] + 2 * np.sin(angle[i])
            ax.imshow(mini_star_icon, extent=[x_pos - 1, x_pos + 1, y_pos - 1, y_pos + 1], aspect='auto')

        # Add text with activity description and time range
        ax.text(x[index], y[index], row['Activity Description'], ha='center', va='center', fontsize=18, color='white')
        ax.text(x[index], y[index] + 1.5, f"{start_time.strftime('%I:%M %p')} - {end_time.strftime('%I:%M %p')}", ha='center', va='top', fontsize=12, color='white')
        
        # Add sparkle trail between activities
        if index < len(df) - 1:
            num_sparkles = 200
            x_sparkles = np.linspace(x[index], x[index + 1], num_sparkles)
            y_sparkles = np.linspace(y[index], y[index + 1], num_sparkles)
            x_sparkles += np.random.uniform(-0.3, 0.3, size=num_sparkles)
            y_sparkles += np.random.uniform(-0.3, 0.3, size=num_sparkles)
            sizes = np.random.rand(num_sparkles) * 15
            colors = np.random.rand(num_sparkles)
            ax.scatter(x_sparkles, y_sparkles, s=sizes, c=colors, marker='*', cmap='cividis', alpha=0.9, zorder=1)

    plt.tight_layout()
    plt.show()

# Draw the timeline
draw_timeline(df, activity_colors)
