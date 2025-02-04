import pygame
import random
import threading
import database  # Import the database module
from database import clear_database

# Constants
WIDTH, HEIGHT = 400, 400
ROWS, COLS = 3, 3
SQUARE_SIZE = WIDTH // COLS
COLORS = {
    'R': (255, 0, 0),
    'G': (0, 255, 0),
    'B': (0, 0, 255),
    'Y': (255, 255, 0),
    'O': (255, 165, 0),
    'W': (255, 255, 255)
}
MOVES = ['U', "U'", 'U2', 'D', "D'", 'D2', 'L', "L'", 'L2', 'R', "R'", 'R2', 'F', "F'", 'F2', 'B', "B'", 'B2']

# Generate a random Rubik's Cube face
def generate_face():
    return [[random.choice(list(COLORS.keys())) for _ in range(COLS)] for _ in range(ROWS)]

# Draw the Rubik's Cube face
def draw_face(face):
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(
                screen,
                COLORS[face[row][col]],
                (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            )
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                1
            )

# Map text to the cube face tiles
def map_text_to_tiles(face, text):
    tiles = []
    clusters = [text[i:i+2] for i in range(0, len(text), 2)]

    for i, cluster in enumerate(clusters):
        if i >= ROWS * COLS:
            break
        row, col = divmod(i, COLS)
        color = face[row][col]
        tile_num = i + 1
        tiles.append(f"{color}{tile_num}={cluster}")

    return tiles

# Encrypt text and shuffle the keys
def encrypt_text(face, text):
    tiles = map_text_to_tiles(face, text)
    random.shuffle(tiles)
    encrypted = ' '.join([tile.split('=')[0] for tile in tiles])

    print("Encryption mapping:")
    for tile in tiles:
        print(tile)
    print("Encrypted text:", encrypted)

    return encrypted

# Generate a 20-move scramble
def generate_scramble():
    return ' '.join(random.choices(MOVES, k=20))

def handle_input(face):
    database.init_db()  # Initialize database
    while True:
        input_text = input("Enter text to encrypt: ")
        if input_text.lower() == 'view':
            database.view_database()
            continue
        encrypted = encrypt_text(face, input_text)
        database.save_to_db(input_text, encrypted)  # Save to database

        if input_text.lower() == 'clear':
            clear_database()
            print("Database cleared.")
            continue

def main():
    clock = pygame.time.Clock()
    running = True

    # Initial face and variables
    face = generate_face()

    # Start the input thread
    input_thread = threading.Thread(target=handle_input, args=(face,), daemon=True)
    input_thread.start()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update face every 5 seconds
        face = generate_face()

        # Draw the face
        screen.fill((0, 0, 0))
        draw_face(face)

        pygame.display.flip()
        clock.tick(1)
    pygame.quit()

if __name__ == "__main__":
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Rubik's Cube Encryption")
    main()