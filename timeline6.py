import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

# Load the data from the CSV file
df = pd.read_csv('24hour.csv')

# Filter data to only include "Day 1"
df = df[df['Day'] == 'Day 1']

# Convert the 'Start time' and 'End time' columns to datetime
df['Start time'] = pd.to_datetime(df['Start time'], format='%m/%d/%Y %I:%M:%S%p', errors='coerce')
df['End time'] = pd.to_datetime(df['end time'], format='%m/%d/%Y %I:%M:%S%p', errors='coerce')

# Define colors for different activity types with a rose gold theme
activity_colors = {
    "sleep": (17, 216, 211),        # Teal
    "relaxing": (255, 182, 193),    # Light Pink Shimmer (for relaxing)
    "travel": (126, 10, 129),       # Purple (for travel)
    "physical-fun": (205, 127, 50), # Copper (for physical fun)
    "mental-fun": (110, 42, 11),    # Maroon (for mental fun)
    "eating": (255, 160, 122),      # Light Salmon (for eating)
    "gaming": (0, 191, 255)         # Electric Blue (for gaming)
}


# Function to generate a spiral path with more space between the points
def generate_spiral_path(num_points, radius):
    theta = np.linspace(0, 6 * np.pi, num_points)  # More rotations for a larger spiral
    r = np.linspace(0, radius, num_points)  # Radial distance increases
    x = r * np.cos(theta)  # X coordinate
    y = r * np.sin(theta)  # Y coordinate
    return x, y

# Function to create a mini star icon with rose gold effect
def create_mini_star(color, size=10, circle_size=20, line_width=3):
    img = Image.new('RGBA', (circle_size, circle_size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Create a gradient rose gold effect for the circle
    gradient = Image.new('RGBA', (circle_size, circle_size), (0, 0, 0, 0))
    gradient_draw = ImageDraw.Draw(gradient)
    
    # Draw a radial gradient (simulating a rose gold metallic shine effect)
    for i in range(circle_size // 2, 0, -1):
        shade = tuple(int(c * (i / (circle_size // 2))) for c in color)  # Apply gradient effect
        gradient_draw.ellipse([i, i, circle_size - i, circle_size - i], outline=shade, width=line_width)
    
    # Apply the gradient to the circle
    img.paste(gradient, (0, 0), gradient)
    
    # Draw the star in the center with the same rose gold tone
    points = [
        (circle_size * 0.5, 0), (circle_size * 0.6, circle_size * 0.35), (circle_size, circle_size * 0.35),
        (circle_size * 0.7, circle_size * 0.6), (circle_size * 0.8, circle_size), (circle_size * 0.5, circle_size * 0.75),
        (circle_size * 0.2, circle_size), (circle_size * 0.3, circle_size * 0.6), (0, circle_size * 0.35), (circle_size * 0.4, circle_size * 0.35)
    ]
    draw.polygon(points, fill=color)
    
    return img

# Function to draw the timeline
def draw_timeline(df, activity_colors):
    fig, ax = plt.subplots(figsize=(36, 24))  # Set the figure size to 36 by 24
    ax.set_xlim(-50, 50)
    ax.set_ylim(-50, 50)
    ax.axis('off')
    fig.patch.set_facecolor('#00008B')

    # Generate a larger spiral path with more space between activities
    x, y = generate_spiral_path(len(df), 30)

    # Add the magic wand at the start (optional, replace the path if you don't want it)
    try:
        magic_wand = Image.open("icons/magicwand.png")
        rotated_wand = magic_wand.rotate(45, expand=True)
        ax.imshow(rotated_wand, extent=[x[0] - 1.5, x[0] + 1.5, y[0] - 1.5, y[0] + 1.5], aspect='auto')
    except FileNotFoundError:
        print("Magic wand image not found!")

    # Create a list to store legend entries with burst numbers
    legend_entries = []

    # For storing the connection between bursts and text
    activity_positions = []

    # Label burst count
    burst_counter = 1

    # We will start the bursts after the first full rotation, or after a certain index
    burst_started = False

    for index, row in df.iterrows():
        start_time, end_time = row['Start time'], row['End time']
        activity_type = row['Activity Type'].split(', ')[0]
        color = activity_colors.get(activity_type, (255, 255, 255, 255))

        if burst_started:
            # Draw mini stars along the spiral outline with rose gold effect
            mini_star_icon = create_mini_star(color, size=1, circle_size=30, line_width=5)
            num_mini_stars = 150  # Number of mini stars around the outline
            angle = np.linspace(0, 2 * np.pi, num_mini_stars, endpoint=False)  # Full circle
            for i in range(num_mini_stars):
                # Create circular positions for mini stars around the main position
                x_pos = x[index] + 2 * np.cos(angle[i])
                y_pos = y[index] + 2 * np.sin(angle[i])
                ax.imshow(mini_star_icon, extent=[x_pos - 1, x_pos + 1, y_pos - 1, y_pos + 1], aspect='auto')

            # Add text with activity description and time range
            activity_description = f"{row['Activity Description']} - {start_time.strftime('%I:%M %p')} to {end_time.strftime('%I:%M %p')}"
            
            # Add burst number to the activity description
            burst_label = f"({burst_counter}) {activity_description}"
            legend_entries.append(burst_label)
            
            # Store activity positions for connection (x and y coordinates)
            activity_positions.append((x[index], y[index]))

            # Label the burst with a number on the spiral
            ax.text(x[index], y[index], str(burst_counter), ha='center', va='center', fontsize=14, color='white', weight='bold')

            burst_counter += 1

        else:
            # Only start the bursts after the first full rotation, or after a certain index
            if index > 5:  # After the spiral has developed a bit
                burst_started = True

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

    # Place the legend outside to the side of the spiral without being cut off
    ax.legend(legend_entries, loc='upper left', bbox_to_anchor=(1.1, 1), fontsize=12, facecolor='black', framealpha=0.5)

    # Save the figure as a PDF
    plt.tight_layout()
    plt.savefig("timeline_visualization.pdf", format="pdf")

    # Show the plot
    plt.show()

# Draw the timeline
draw_timeline(df, activity_colors)
