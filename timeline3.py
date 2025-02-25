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

# Function to generate a left-to-right twirling path
def generate_twirling_path(num_points, radius):
    theta = np.linspace(0, 8 * np.pi, num_points)  # Create a smooth curve for twirling
    x = np.linspace(-15, 15, num_points)  # Spread points from left to right
    y = radius * np.sin(theta)  # Sinusoidal curve to make the path twirl down the page
    return x, y

# Function to create a star-shaped icon (used in place of the rectangle)
def create_star(color, size=60):
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))  # Transparent background
    draw = ImageDraw.Draw(img)

    # Create a 5-point star shape
    points = [
        (size * 0.5, 0),  # top point
        (size * 0.6, size * 0.35),
        (size, size * 0.35),  # right point
        (size * 0.7, size * 0.6),
        (size * 0.8, size),  # bottom-right point
        (size * 0.5, size * 0.75),
        (size * 0.2, size),  # bottom-left point
        (size * 0.3, size * 0.6),
        (0, size * 0.35),  # left point
        (size * 0.4, size * 0.35),
    ]
    
    draw.polygon(points, fill=color)
    return img

# Function to draw the timeline
def draw_timeline(df, activity_colors):
    fig, ax = plt.subplots(figsize=(24, 36))  # Set figure size to match 24x36 inch print
    ax.set_xlim(-20, 20)  # Spread out across the larger canvas
    ax.set_ylim(-40, 40)  # Spread out vertically
    ax.axis('off')

    # Set the background color to dark blue
    fig.patch.set_facecolor('#00008B')  # Dark blue color for the background

    # Generate smoother twirling path coordinates (adjusting for left-to-right movement)
    x, y = generate_twirling_path(len(df), 20)  # Increase radius to ensure more spacing

    # Add the magic wand image at the start of the timeline, pointing towards the first activity
    magic_wand = Image.open("icons/magicwand.png")
    rotated_wand = magic_wand.rotate(45, expand=True)  # Rotate the wand by 45 degrees
    ax.imshow(rotated_wand, extent=[x[0] - 1.5, x[0] + 1.5, y[0] - 1.5, y[0] + 1.5], aspect='auto')

    # Start the first activity, "Get to hotel and sleep"
    for index, row in df.iterrows():
        start_time = row['Start time']
        end_time = row['end time']
        activity_type = row['Activity Type'].split(', ')[0]  # Get the first activity type
        color = activity_colors.get(activity_type, (255, 255, 255, 255))  # Default color if none found

        # Create regular star-shaped icons for all activities
        star_icon = create_star(color, size=60)
        ax.imshow(star_icon, extent=[x[index] - 3, x[index] + 3, y[index] - 3, y[index] + 3], aspect='auto', zorder=2)

        # Display the activity description text near the icon (inside the star)
        ax.text(x[index], y[index], row['Activity Description'], ha='center', va='center', fontsize=18, zorder=3, color="white")

        # Add start and end time labels near the icon (inside the star)
        start_time_label = start_time.strftime('%I:%M %p')
        end_time_label = end_time.strftime('%I:%M %p')
        ax.text(x[index], y[index] + 1.5, f"{start_time_label} - {end_time_label}", ha='center', va='top', fontsize=12, color='white')

        # Add sparkle trail between consecutive activities
        if index < len(df) - 1:
            # Generate sparkles along the path between current and next activity
            num_sparkles = 200  # Increase the number of sparkles for higher density
            x_sparkles = np.linspace(x[index], x[index + 1], num_sparkles)
            y_sparkles = np.linspace(y[index], y[index + 1], num_sparkles)

            # Create overlap effect by making sparkles closer together
            overlap_factor = 0.3
            x_sparkles += np.random.uniform(-overlap_factor, overlap_factor, size=num_sparkles)
            y_sparkles += np.random.uniform(-overlap_factor, overlap_factor, size=num_sparkles)

            sizes = np.random.rand(num_sparkles) * 15  # Smaller sparkles for higher density
            colors = np.random.rand(num_sparkles)  # Random colors for sparkle effect

            # Scatter the sparkles along the path, ensuring overlap and higher density
            ax.scatter(x_sparkles, y_sparkles, s=sizes, c=colors, marker='*', cmap='cividis', alpha=0.9, zorder=1)

    plt.tight_layout()
    plt.show()

# Draw the timeline
draw_timeline(df, activity_colors)
