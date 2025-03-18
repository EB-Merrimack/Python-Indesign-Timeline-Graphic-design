import os
import numpy as np
from PIL import Image, ImageDraw

# Function to create a single mini star with a circular gradient
def create_mini_star(color, circle_size=40, line_width=4):
    img = Image.new('RGBA', (circle_size, circle_size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # Create a gradient effect inside the circle
    gradient = Image.new('RGBA', (circle_size, circle_size), (0, 0, 0, 0))
    gradient_draw = ImageDraw.Draw(gradient)

    # Draw a radial gradient (simulating a metallic shine effect)
    for i in range(circle_size // 2, 0, -1):
        shade = tuple(int(c * (i / (circle_size // 2))) for c in color)  # Apply gradient effect
        gradient_draw.ellipse([i, i, circle_size - i, circle_size - i], outline=shade, width=line_width)

    # Apply the gradient to the circle
    img.paste(gradient, (0, 0), gradient)

    # Draw a centered star inside the circle
    points = [
        (circle_size * 0.5, circle_size * 0.1), (circle_size * 0.6, circle_size * 0.35),
        (circle_size * 0.9, circle_size * 0.35), (circle_size * 0.65, circle_size * 0.55),
        (circle_size * 0.75, circle_size * 0.85), (circle_size * 0.5, circle_size * 0.7),
        (circle_size * 0.25, circle_size * 0.85), (circle_size * 0.35, circle_size * 0.55),
        (circle_size * 0.1, circle_size * 0.35), (circle_size * 0.4, circle_size * 0.35)
    ]
    draw.polygon(points, fill=color)

    return img

# Function to arrange condensed mini stars in a circular formation
def create_condensed_mini_star_swirl(color, num_mini_stars=180, radius=50, circle_size=15):
    img_size = (radius * 2 + circle_size, radius * 2 + circle_size)
    img = Image.new('RGBA', img_size, (255, 255, 255, 0))
    
    angle_steps = np.linspace(0, 2 * np.pi, num_mini_stars, endpoint=False)  # Full circle
    center = (img_size[0] // 2, img_size[1] // 2)

    for angle in angle_steps:
        x = int(center[0] + radius * np.cos(angle) - circle_size // 2)
        y = int(center[1] + radius * np.sin(angle) - circle_size // 2)
        
        mini_star = create_mini_star(color, circle_size)
        img.paste(mini_star, (x, y), mini_star)

    return img

# Define activity colors with a rose gold theme
activity_colors = {
    "relaxing": (255, 210, 220),    # Light Pink Shimmer
    "travel": (160, 30, 180),       # Purple
    "mental-fun": (110, 42, 11),    # Maroon
    "physical-fun": (110, 42, 11),  # Maroon (same as mental-fun)
    "eating": (0, 128, 128),        # Rich Teal
    "clifton hill": (255, 140, 0)   # Strong Orange
}

# Create output directory if not exists
output_dir = "legend_mini_star_swirls"
os.makedirs(output_dir, exist_ok=True)

# Generate and save condensed circular star swirls for each activity type
for activity, color in activity_colors.items():
    swirl_img = create_condensed_mini_star_swirl(color, num_mini_stars=180, radius=50, circle_size=12)

    # Save the image as PNG with a transparent background
    swirl_img.save(os.path.join(output_dir, f"{activity}_mini_star_swirl.png"), "PNG")

print("Condensed mini star swirl legends saved successfully!")
