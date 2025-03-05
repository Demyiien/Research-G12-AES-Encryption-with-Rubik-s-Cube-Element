import pygame
from encryption import generate_face  # Import the cube generation function

# Visualization settings
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

def draw_face(screen, face):
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

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Rubik's Cube Visualization")
    clock = pygame.time.Clock()
    running = True

    while running:
        face = generate_face()  # Generate a new cube face
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        draw_face(screen, face)
        pygame.display.flip()
        clock.tick(1)  # Update the display every second
    pygame.quit()

if __name__ == "__main__":
    main()
