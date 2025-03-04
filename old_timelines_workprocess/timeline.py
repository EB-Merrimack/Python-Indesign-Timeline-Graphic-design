import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import numpy as np

# Load the data from the CSV file
df = pd.read_csv('24hour.csv')

# Filter data to only include "Day 1"
df = df[df['Day'] == 'Day 1']

# Convert the 'Start time' and 'end time' columns to datetime
df['Start time'] = pd.to_datetime(df['Start time'], format='%m/%d/%Y %I:%M:%S%p', errors='coerce')
df['end time'] = pd.to_datetime(df['end time'], format='%m/%d/%Y %I:%M:%S%p', errors='coerce')

# Function to create a star image
def create_star_image(color, size=(20, 20)):
    img = Image.new('RGBA', size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    draw.polygon([(size[0]//2, 0), (size[0]*3//8, size[1]//2), (0, size[1]//2), 
                  (size[0]*3//8, size[1]*3//4), (size[0]//4, size[1]), 
                  (size[0]//2, size[1]*5//8), (size[0]*3//4, size[1]), 
                  (size[0]*5//8, size[1]*3//4), (size[0], size[1]//2), 
                  (size[0]*5//8, size[1]//2)], fill=color)
    return img

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

# Create a function to generate swirling path coordinates
def generate_swirling_path(num_points, radius):
    theta = np.linspace(0, 4 * np.pi, num_points)
    r = np.linspace(0, radius, num_points)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y

# Create a function to draw the timeline
def draw_timeline(df, activity_colors):
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.axis('off')
    
    # Generate swirling path coordinates
    x, y = generate_swirling_path(len(df), 10)
    
    # Plot the timeline path
    for i in range(len(df)):
        ax.plot(x[:i+1], y[:i+1], color='purple', linewidth=2)
        ax.scatter(x[:i+1], y[:i+1], color='purple', s=50, zorder=5)
    
    # Plot each activity
    for index, row in df.iterrows():
        start_time = row['Start time']
        end_time = row['end time']
        activity_type = row['Activity Type'].split(', ')[0]
        color = activity_colors.get(activity_type, (255, 255, 255, 255))
        left_pos = start_time.hour + start_time.minute / 60
        
        # Plot the activity description with star icon
        star_icon = create_star_image(color)
        ax.imshow(star_icon, extent=[x[index] - 0.5, x[index] + 0.5, y[index] - 0.5, y[index] + 0.5], aspect='auto')
        ax.text(x[index], y[index], row['Activity Description'], ha='center', va='center', fontsize=10, zorder=10)

    plt.tight_layout()
    plt.show()

# Draw the timeline
draw_timeline(df, activity_colors)
