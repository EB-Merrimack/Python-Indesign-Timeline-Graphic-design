import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from PIL import Image

# Function to generate spiral path
def generate_spiral_path(num_points, radius):
    theta = np.linspace(0, 6 * np.pi, num_points)  # More rotations for a larger spiral
    
    # Adjusting the radial distance to increase the space between spirals
    r = np.linspace(0, radius, num_points) ** 1.7  # Increase the exponent to widen the spiral faster
    x = r * np.cos(theta)  # X coordinate
    y = r * np.sin(theta)  # Y coordinate

    # Re-centering the spiral by shifting it to the middle of the plot
    x_centered = x - x.min()  # Shift by the minimum value to center the spiral horizontally
    y_centered = y - y.min()  # Shift by the minimum value to center the spiral vertically

    return x_centered, y_centered

# Function to create a gold star
def create_star(center_x, center_y, size, color='gold'):
    angles = np.linspace(0, 2 * np.pi, 11)  # 10 points + closing point
    radius_outer = size
    radius_inner = size / 2.5

    star_points = []
    for i, angle in enumerate(angles[:-1]):  # Skip last point to avoid duplication
        radius = radius_outer if i % 2 == 0 else radius_inner
        star_points.append((center_x + radius * np.cos(angle), center_y + radius * np.sin(angle)))

    return Polygon(star_points, closed=True, facecolor=color, edgecolor='black', lw=1.5, zorder=3)

# Load the magic wand image
magic_wand = Image.open("icons/bigger_wand_withstart.png")

# Resize the image (increase the width and height to make it larger)
new_width = 500  # Increase the width to make it larger
new_height = 500  # Increase the height to make it larger
resized_wand = magic_wand.resize((new_width, new_height), Image.Resampling.LANCZOS)

# Rotate the resized image if necessary
rotated_wand = resized_wand.rotate(0, expand=True)  # Rotate if needed (0 degrees in this case)

# Generate the spiral path
x_spiral, y_spiral = generate_spiral_path(num_points=150, radius=15)  # Increased radius for a larger spiral

# Function to create a larger sparkle trail between activities
def create_sparkle_trail(ax, x, y, num_sparkles=500):  # Increased num_sparkles for a larger trail
    for index in range(len(x) - 1):
        # Generate sparkle points between consecutive activities
        x_sparkles = np.linspace(x[index], x[index + 1], num_sparkles)
        y_sparkles = np.linspace(y[index], y[index + 1], num_sparkles)
        x_sparkles += np.random.uniform(-0.5, 0.5, size=num_sparkles)  # Larger random offset
        y_sparkles += np.random.uniform(-0.5, 0.5, size=num_sparkles)  # Larger random offset
        sizes = np.random.rand(num_sparkles) * 30  # Larger size for sparkles
        colors = np.random.rand(num_sparkles)
        ax.scatter(x_sparkles, y_sparkles, s=sizes, c=colors, marker='*', cmap='cividis', alpha=0.9, zorder=-1)

# Function to add single gold stars along the path
def add_single_gold_stars(ax, x, y, num_stars=8, star_size_range=(12, 13), start_after=10, space_between=5):
    # Select indices with space between them
    star_indices = range(start_after, len(x), space_between)  # Choose single stars with spacing
    x_stars = x[star_indices]
    y_stars = y[star_indices]
    
    # Plot the stars with large sizes and gold color
    for x_star, y_star in zip(x_stars, y_stars):
        star_size = np.random.randint(*star_size_range)  # Random size for each star
        star = create_star(x_star, y_star, star_size, color='gold')
        ax.add_patch(star)  # Add the star as a patch to the plot

# Plotting setup
fig, ax = plt.subplots(figsize=(40, 32))  # Increased the figure size
ax.set_xlim(-50, 250)  # Adjusted limits to provide more space
ax.set_ylim(-50, 250)  # Adjusted limits to provide more space
ax.axis('off')  # Hide the axes

# Plot the spiral path
ax.plot(x_spiral, y_spiral, color='gray', lw=2, zorder=1)

# Add sparkle trail starting from the wand's tip (wand's tip is the first point of the spiral)
create_sparkle_trail(ax, x_spiral, y_spiral)

# Add single gold stars along the path, starting after the 50th point, with space between them
add_single_gold_stars(ax, x_spiral, y_spiral, num_stars=8, star_size_range=(12, 13), start_after=50, space_between=9)

# Add the wand image at the start of the spiral (position 0) to represent the tip
wand_x = x_spiral[0]
wand_y = y_spiral[0] - 10  # Move the wand down further from its original position for more space

# Convert image to numpy array for display in Matplotlib
wand_array = np.array(rotated_wand)

# Display the wand image at the start of the spiral (wand's tip)
ax.imshow(wand_array, extent=(wand_x - 25, wand_x + 25, wand_y - 25, wand_y + 25), aspect='auto', zorder=10)

# Save the figure to a vector format (SVG)
plt.savefig("spiral_magic_wand_centered.svg", format="svg", bbox_inches='tight')  # Save as SVG

# Show the plot
plt.show()
