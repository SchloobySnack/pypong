import asyncio
import pygame
import random

pygame.init()
width = 640  # Adjust width and height as needed
height = 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Rectangle")

WHITE = (255, 255, 255)  # Color for white rectangle

async def main():
  # Game variables
  rect_x = 100
  rect_y = 100
  rect_width = 50
  rect_height = 20
  x_speed = 5  # Adjust for desired horizontal speed
  y_speed = 30  # Adjust for desired vertical speed
  running = True
  rect_initialized = False
  clock = pygame.time.Clock()  # Create a clock object

  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False

    # Get delta time (time elapsed since last frame)
    delta_time = clock.tick(60) / 1000  # Get time in seconds

    # Screen fill (optional)
    screen.fill((0, 0, 0))

    if not rect_initialized:
      rect_y = 100  # Initialize on first iteration only
      rect_initialized = True

    # Update rectangle position using delta_time
    rect_x += x_speed * delta_time
    rect_y += y_speed * delta_time

    # Check for left/right screen collision and bounce
    if rect_x <= 0 or rect_x + rect_width >= width:
      x_speed = -x_speed  # Invert x-speed for bounce

    # Check for top/bottom screen collision and bounce with randomness
    if rect_y <= 0:
      rect_y = 0
      y_speed = -y_speed * (1 + random.uniform(-0.1, 0.1))  # Bounce with randomness
    elif rect_y + rect_height >= height:
      rect_y = height - rect_height
      y_speed = -y_speed * (1 + random.uniform(-0.1, 0.1))  # Bounce with randomness

    # Draw the rectangle with updated position
    pygame.draw.rect(screen, WHITE, (rect_x, rect_y, rect_width, rect_height))

    pygame.display.flip()

    await asyncio.sleep(0)

  pygame.quit()

asyncio.run(main())
