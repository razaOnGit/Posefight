from PIL import Image
import os

# Set the folder where your images are stored
folder = "assets/sprites/"

# Loop through all files in the folder
for filename in os.listdir(folder):
    if filename.endswith(".webp"):  # Check if file is a .webp image
        img = Image.open(os.path.join(folder, filename))  # Open image
        new_filename = filename.replace(".webp", ".png")  # Change extension
        img.save(os.path.join(folder, new_filename), "PNG")  # Save as PNG
        print(f"Converted {filename} → {new_filename}")  # Print success message
