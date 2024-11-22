import streamlit as st
import random
import time

# Initialize session state variables
if "grid_size" not in st.session_state:
    st.session_state.grid_size = 10

if "black_pixel_count" not in st.session_state:
    st.session_state.black_pixel_count = 30

# Custom CSS for styling
st.markdown(
    """
    <style>
    .centered-title {
        text-align: center;
        font-size: 32px;
        font-weight: bold;
    }
    .controls {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .control-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        font-family: Arial, sans-serif;
    }
    .centered-grid {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .grid-row {
        display: flex;
        justify-content: center;
        font-family: monospace;
    }
    .grid-cell {
        width: 25px;
        height: 25px;
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
        margin: 2px;
    }
    .black-cell {
        background-color: black;
        color: black;
    }
    .white-cell {
        background-color: white;
        color: white;
        border: 1px solid lightgray;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# App title
st.markdown('<div class="centered-title">Gravchamber</div>', unsafe_allow_html=True)

# Controls for grid size and black pixel count
st.markdown('<div class="controls">', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    st.session_state.grid_size = st.number_input(
        "Grid Size", min_value=5, max_value=20, value=st.session_state.grid_size, step=1, key="grid_size_input"
    )

with col2:
    st.session_state.black_pixel_count = st.number_input(
        "Black Pixels", min_value=1, max_value=st.session_state.grid_size ** 2 - 1, value=st.session_state.black_pixel_count, step=1, key="black_pixel_input"
    )
st.markdown("</div>", unsafe_allow_html=True)

# Gravity slider with max at 0.99
gravity = st.slider("Gravity", 0.0, 0.99, 0.3)

# Initialize the grid
grid_size = st.session_state.grid_size
black_pixel_count = st.session_state.black_pixel_count

if "grid" not in st.session_state or len(st.session_state.grid) != grid_size:
    st.session_state.grid = [["white" for _ in range(grid_size)] for _ in range(grid_size)]
    st.session_state.black_pixels = set()
    while len(st.session_state.black_pixels) < min(black_pixel_count, grid_size * grid_size):
        x, y = random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)
        if (x, y) not in st.session_state.black_pixels:
            st.session_state.black_pixels.add((x, y))
            st.session_state.grid[y][x] = "black"

# Ensure the number of black pixels matches the user input
while len(st.session_state.black_pixels) < black_pixel_count:
    x, y = random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)
    if st.session_state.grid[y][x] == "white":
        st.session_state.grid[y][x] = "black"
        st.session_state.black_pixels.add((x, y))

while len(st.session_state.black_pixels) > black_pixel_count:
    x, y = st.session_state.black_pixels.pop()
    st.session_state.grid[y][x] = "white"

# Function to move black pixels
def move_pixels():
    new_positions = set()
    for x, y in st.session_state.black_pixels:
        # Calculate movement
        dx, dy = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
        if random.random() < gravity:
            dy += 1  # Gravity pulls pixels down

        new_x, new_y = x + dx, y + dy

        # Ensure the new position is within bounds
        new_x = max(0, min(grid_size - 1, new_x))
        new_y = max(0, min(grid_size - 1, new_y))

        # Move pixel only if the position is empty (white)
        if st.session_state.grid[new_y][new_x] == "white":
            st.session_state.grid[y][x] = "white"
            st.session_state.grid[new_y][new_x] = "black"
            new_positions.add((new_x, new_y))
        else:
            new_positions.add((x, y))

    st.session_state.black_pixels = new_positions

# Main loop to animate the pixels
placeholder = st.empty()

while True:
    move_pixels()

    # Render the grid
    with placeholder.container():
        st.markdown('<div class="centered-grid">', unsafe_allow_html=True)
        for row in st.session_state.grid:
            row_html = '<div class="grid-row">'
            for cell in row:
                cell_class = "black-cell" if cell == "black" else "white-cell"
                row_html += f'<div class="grid-cell {cell_class}"></div>'
            row_html += "</div>"
            st.markdown(row_html, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Pause for 0.25 seconds
    time.sleep(0.20)
