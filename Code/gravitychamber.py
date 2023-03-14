import tkinter as tk
import random

# Define the size of the grid
grid_size = 10

# Create a new Tkinter window
root = tk.Tk()

# Set the title of the window
root.title("Moving Pixels")

# Create a canvas widget
canvas = tk.Canvas(root, width=500, height=500)

# Create a grid of white pixels
for i in range(grid_size):
    for j in range(grid_size):
        x1 = i * 50
        y1 = j * 50
        x2 = x1 + 50
        y2 = y1 + 50
        fill_color = "white"
        if i == grid_size//2 and j == grid_size//2:
            pass
            # fill_color = "black"
        canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color)

# Create 30 black pixels at random positions
black_pixels = []
for i in range(30):
    x, y = random.randint(1, grid_size - 2), random.randint(1, grid_size - 2)
    while canvas.itemcget(canvas.find_closest(x * 50 + 25, y * 50 + 25), "fill") == "black":
        x, y = random.randint(1, grid_size - 2), random.randint(1, grid_size - 2)
    x1 = x * 50
    y1 = y * 50
    x2 = x1 + 50
    y2 = y1 + 50
    black_pixels.append(canvas.create_rectangle(x1, y1, x2, y2, fill="black"))


# Create a slider for controlling the gravity parameter
gravity_scale = tk.Scale(root, from_=0.0, to=1.0, resolution=0.01, orient=tk.HORIZONTAL, label="Gravity")
gravity_scale.pack()

# Pack the canvas widget into the window
canvas.pack()

# Define a function to move the black pixels
def move_pixels():
    for pixel in black_pixels:
        # Get the current position of the pixel
        x1, y1, x2, y2 = canvas.coords(pixel)
        x = x1 // 50
        y = y1 // 50
        # Choose a random direction to move
        dx, dy = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
        # Adjust the dy value based on the current y position and gravity coefficient
        gravity = gravity_scale.get()/3
        dy += int((grid_size - y) * gravity)
        # Check if there is another black pixel in the way of the chosen direction
        if dx == 1 and canvas.itemcget(canvas.find_closest(x2 + 25, y1 + 25), "fill") == "black":
            dx = 0
        elif dx == -1 and canvas.itemcget(canvas.find_closest(x1 - 25, y1 + 25), "fill") == "black":
            dx = 0
        elif dy == 1 and canvas.itemcget(canvas.find_closest(x1 + 25, y2 + 25), "fill") == "black":
            dy = 0
        elif dy == -1 and canvas.itemcget(canvas.find_closest(x1 + 25, y1 - 25), "fill") == "black":
            dy = 0
        # Move the pixel
        new_x = x + dx
        new_y = y + dy
        if new_x < 0:
            new_x = 0
        elif new_x >= grid_size:
            new_x = grid_size - 1
        if new_y < 0:
            new_y = 0
        elif new_y >= grid_size:
            new_y = grid_size - 1
        # Check if there is an adjacent white pixel
        if canvas.itemcget(canvas.find_closest(new_x * 50 + 25, new_y * 50 + 25), "fill") == "white":
            new_x1 = new_x * 50
            new_y1 = new_y * 50
            new_x2 = new_x1 + 50
            new_y2 = new_y1 + 50
            canvas.coords(pixel, new_x1, new_y1, new_x2, new_y2)

    # Schedule the move_pixels function to run again in 1 second
    root.after(100, move_pixels)

# Schedule the move_pixels function to run after 1 second
root.after(100, move_pixels)

# Start the main event loop
root.mainloop()
