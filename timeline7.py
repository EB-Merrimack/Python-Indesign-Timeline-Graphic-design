import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFilter
from matplotlib.patches import Polygon
import textwrap

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
    "relaxing": (255, 182, 193),    # Light Pink Shimmer (for relaxing)
    "travel": (126, 10, 129),       # Purple (for travel)
    "mental-fun": (110, 42, 11),    # Maroon (for mental fun)
    "physical-fun": (110, 42, 11), # use the same for both fun icons
    "eating": (255, 160, 122),      # Light Salmon (for eating)
    "gaming": (0, 191, 255)         # Electric Blue (for gaming)
}

# Function to generate a spiral path with more space between the points
# Function to generate a spiral path with more space between the points
def generate_spiral_path(num_points, radius):
    theta = np.linspace(0, 6 * np.pi, num_points)  # More rotations for a larger spiral
    
    # Adjusting the radial distance to increase the space between spirals
    r = np.linspace(0, radius, num_points) ** 1.1 
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

# Function to create a 5-point burst star
def create_star(center_x, center_y, size, color='gold'):
    angles = np.linspace(0, 2 * np.pi, 11)  # 10 points + closing point
    radius_outer = size
    radius_inner = size / 2.5

    star_points = []
    for i, angle in enumerate(angles[:-1]):  # Skip last point to avoid duplication
        radius = radius_outer if i % 2 == 0 else radius_inner
        star_points.append((center_x + radius * np.cos(angle), center_y + radius * np.sin(angle)))

    return Polygon(star_points, closed=True, facecolor=color, edgecolor='black', lw=1.5, zorder=3)

# Function to create a sleep icon (e.g., a moon)# Function to create a sleep icon (use an existing image, e.g., sleep.png)
# Function to create a sleep icon (use the original image, e.g., sleep.png)
def create_sleep_icon( ):
    img = Image.open("icons/sleep.png")
    
    # Return the image without resizing
    return img

#Function to create carriage icon
def create_carriage():
    img = Image.open("icons/carriage.png")
    return img
 #function to create slipper / walking icon
 
def create_slipper():
     img = Image.open("icons/glassslipper_walking.png")
     return img

# Function to create a physical fun icon (use the original image, e.g., sleep.png)
def create_physical_fun_icon( ):
    
    img = Image.open("icons/female_mouse_physical.png")
    
    # Return the image without resizing
    return img


def draw_timeline(df, activity_colors):
    fig, ax = plt.subplots(figsize=(36, 24))  # Set the figure size to 36 by 24
    ax.set_xlim(-50, 50)
    ax.set_ylim(-50, 50)
    ax.axis('off')

    # Generate a larger spiral path with more space between activities
    x, y = generate_spiral_path(len(df), 30)

    try:
        magic_wand = Image.open("icons/bigger_wand.png")

        # Resize the image (increase the width and height to make it larger)
        new_width = 500  # Increase the width to make it larger
        new_height = 500  # Increase the height to make it larger
        resized_wand = magic_wand.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Rotate the resized image if necessary
        rotated_wand = resized_wand.rotate(80, expand=True)

        # Adjust the x and y-axis extents to move the image
        x_offset = 5  # Adjust this value to move the image left or right
        y_offset = 4  # Adjust this value to move the image up or down
        
        ax.imshow(rotated_wand, extent=[x[0] - 10 + x_offset, x[0] + 10 + x_offset, y[0] - 20 + y_offset, y[0] + 20 + y_offset], aspect='auto')

        # Generate a small burst of stars around the wand
        num_stars_burst = 50  # Number of stars in the burst
        mini_star_icon = create_mini_star((255, 215, 0), size=1, circle_size=30, line_width=5)  # Gold color for burst

        # Use the same size logic for the burst stars
        sizes_burst = np.random.rand(num_stars_burst) * 15  # Match the size range of the path stars

        angle_burst = np.linspace(0, 2 * np.pi, num_stars_burst, endpoint=False)
        for j in range(num_stars_burst):
            # Randomize the positions for the burst effect
            x_pos = x[0] + 3 * np.cos(angle_burst[j]) + np.random.uniform(-1, 1)
            y_pos = y[0] + 3 * np.sin(angle_burst[j]) + np.random.uniform(-1, 1)

            # Draw the burst stars with randomized sizes
            ax.scatter(x_pos, y_pos, s=sizes_burst[j], c='gold', marker='*', alpha=0.9, zorder=1)

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
        activity_types = row['Activity Type'].split(', ')  # Handle multiple activity types
        color = activity_colors.get(activity_types[0], (255, 255, 255, 255))

        if burst_started:
            num_stars = len(activity_types)
            
            for i in range(num_stars):
                color = activity_colors.get(activity_types[i], (255, 255, 255, 255))
                
                if activity_types[i] == "sleep":
                    sleep_icon = create_sleep_icon()
                    x_offset = (i - (num_stars // 2)) * 2
                    ax.imshow(sleep_icon, extent=[x[index] + x_offset - 2, x[index] + x_offset + 2, y[index] - 2, y[index] + 2], aspect='auto')

                elif activity_types[i] == "travel":
                    activity_description = row['Activity Description'].lower()

                    # Create burst star for travel activities
                    travel_star = create_star(x[index], y[index] - 4, size=5)
                    travel_star.set_zorder(0)  # Place behind other elements
                    ax.add_patch(travel_star)

                    # Choose travel icon
                    if "car ride" in activity_description:
                        travel_icon = create_carriage()
                    else:
                        travel_icon = create_slipper()

                    # Place travel icon inside the burst star
                    ax.imshow(travel_icon, extent=[x[index] - 1.2, x[index] + 1.2, y[index] - 4.5, y[index] - 2.5], aspect='auto', zorder=1)

                elif activity_types[i] in ["physical-fun", "mental-fun"]:
                    # Determine fun icon
                    if activity_types[i] == "physical-fun":
                        fun_icon = create_physical_fun_icon()
                    else:
                        fun_icon = create_mental_fun_icon()

                    # Place fun icon at the same y-offset where bursts were
                    ax.imshow(fun_icon, extent=[x[index] - 1.5, x[index] + 1.5, y[index] - 4.5, y[index] - 2.5], aspect='auto', zorder=1)

                    
           
            # Check if the activity type has a corresponding color before creating mini stars
                if activity_types[i] in activity_colors:
                    mini_star_icon = create_mini_star(color, size=2, circle_size=50, line_width=5)
                    x_offset = (i - (num_stars // 2)) * 2  # Spread the stars apart
                    num_mini_stars = 150  # Number of mini stars around the outline
                    angle = np.linspace(0, 2 * np.pi, num_mini_stars, endpoint=False)  # Full circle
                    
                    for j in range(num_mini_stars):
                        # Calculate positions for mini stars around the burst star's position
                        radius = 5  # Radius around the burst star
                        x_pos = x[index] + radius * np.cos(angle[j]) + x_offset
                        y_pos = y[index] - 5 + radius * np.sin(angle[j]) + 2  # Adjust vertical offset as needed
                        
                        # Place the mini stars around the burst star
                        ax.imshow(mini_star_icon, extent=[x_pos - 1, x_pos + 1, y_pos - 1, y_pos + 1], aspect='auto', zorder=-1)
            # Add text with activity description and time range
            activity_description = f"{', '.join(activity_types)} - {start_time.strftime('%I:%M %p')} to {end_time.strftime('%I:%M %p')}"
            
            # Add burst number to the activity description
            burst_label = f"({burst_counter}) {activity_description}"
            legend_entries.append(burst_label)
            
            # Store activity positions for connection (x and y coordinates)
            activity_positions.append((x[index], y[index]))

        
            # Function to wrap text to fit within the star
            def wrap_text(text, width=10):
                return textwrap.fill(text, width=width)

            # Loop through your dataset and process each activity
            activity_description = row['Activity Description']

            # Check if the activity description contains "sleep" or "car ride"
            if "sleep" not in activity_description.lower() and "car ride" not in activity_description.lower() and "walking" not in activity_description.lower():
                # Create the burst star (adjusted position) for activities that aren't "sleep" or "car ride"
                burst_star = create_star(x[index], y[index] - 4, size=6)  # Decreased size and adjusted position
                burst_star.set_zorder(0)  # Set zorder to 0 to place it behind other elements
                ax.add_patch(burst_star)

                # Wrap the activity description text to fit within the star
                wrapped_description = wrap_text(activity_description)

                # Display the wrapped text
                ax.text(x[index], y[index] - 4, wrapped_description, ha='center', va='center', fontsize=5, color='white', weight='bold', wrap=True, zorder=1)

                burst_counter += 1
            else:
                # For "sleep" or "car ride", still count the spot in the spiral but don't create the burst star or display the text
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
            ax.scatter(x_sparkles, y_sparkles, s=sizes, c=colors, marker='*', cmap='cividis', alpha=0.9, zorder=-1)

    # Place the legend outside to the side of the spiral without being cut off
    ax.legend(legend_entries, loc='upper left', bbox_to_anchor=(1.1, 1), fontsize=12, facecolor='black', framealpha=0.5)

    # Save the figure as a PDF
    plt.tight_layout()
    plt.savefig("timeline_visualization.pdf", format="pdf")

    # Show the plot
    plt.show()

# Draw the timeline
draw_timeline(df, activity_colors)
