import asyncio
import pygame
import random

pygame.init()
width = 640  # Adjust width and height as needed
height = 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Ball")

WHITE = (255, 255, 255)  # Color for ball
GRAY = (128, 128, 128)  # Color for paddle

first_iteration = True
score_display_active = False
score = 0


def draw_objects(ball_x, ball_y, ball_width, ball_height, paddle_x, paddle_y, paddle_width, paddle_height):
  """
  Draws the ball, paddle, and score (if active) on the screen.
  """
  pygame.draw.rect(screen, WHITE, (ball_x, ball_y, ball_width, ball_height))
  pygame.draw.rect(screen, GRAY, (paddle_x, paddle_y, paddle_width, paddle_height))

  if score_display_active:
    draw_score_display(score)


def draw_score_display(score):
  """
  Draws a temporary score display on the screen with a fading effect.
  """
  font = pygame.font.Font(None, 50)  # Choose a system font or load a custom font
  score_text = font.render("+" + str(score), True, (255, 255, 255))  # White text

  # Get screen size
  screen_width, screen_height = screen.get_size()

  # Calculate text position based on screen size
  text_x = (screen_width - score_text.get_width()) // 2
  text_y = (screen_height - score_text.get_height()) // 2

  # Create a transparent surface for the score display
  alpha = int(255 - score_display_time * 2.55)  # Adjust fade speed (higher = faster fade)
  score_surface = pygame.Surface(score_text.get_size(), pygame.SRCALPHA)  # Transparent
  score_surface.fill((0, 0, 0, alpha))  # Fill with transparent black with fading alpha

  # Blit text onto the transparent surface
  score_surface.blit(score_text, (0, 0))

  # Blit the score surface with fading effect onto the main screen
  screen.blit(score_surface, (text_x, text_y))


def handle_ball_movement(ball_x, ball_y, ball_width, ball_height, x_speed, y_speed, delta_time, first_iteration):
  """
  Updates the ball's position based on speed and delta time, handling collisions with walls and setting a random starting x-position on respawn.
  """
  ball_x += x_speed * delta_time
  ball_y += y_speed * delta_time

  # Check for left/right screen collision and bounce
  if ball_x <= 0 or ball_x + ball_width >= width:
    x_speed = -x_speed

  # Check for top screen collision and bounce with randomness
  if ball_y <= 0:
    ball_y = 0
    y_speed = -y_speed * (1 + random.uniform(-0.1, 0.1))  # Bounce with randomness

  # Respawn ball with random x-position (within screen bounds) and keep y-position fixed
  elif ball_y + ball_height >= height:
    ball_x = random.randint(ball_width // 2, width - ball_width // 2)  # Ensures ball stays within screen
    ball_y = 100  # Adjust this value for your desired fixed y-position

  return ball_x, ball_y, x_speed, y_speed


def handle_paddle_movement(paddle_x, paddle_y, paddle_width, mouse_x):
  """
  Updates the paddle's position based on mouse movement, ensuring it stays within screen bounds.
  """
  paddle_x = mouse_x - paddle_width // 2  # Center paddle rectangle on cursor

  # Ensure paddle rectangle stays within screen bounds (x-axis)
  paddle_x = max(0, min(paddle_x, width - paddle_width))

  return paddle_x, paddle_y


def handle_collisions(ball_x, ball_y, ball_width, ball_height, paddle_x, paddle_y, paddle_width, y_speed):
  """
  Checks for ball collision with the paddle and updates y-speed and score if collision occurs.
  """
  if ball_x + ball_width >= paddle_x and ball_x <= paddle_x + paddle_width and \
     ball_y + ball_height >= paddle_y:
    y_speed = -y_speed  # Bounce the ball
    global score  # Access global score variable
    score += 1  # Increase score on successful paddle hit
    score_display_active = True  # Activate score display
    score_display_time = 0  # Reset timer

  return y_speed


async def main():
  # Game variables
  ball_x = 100
  ball_y = 100
  ball_width = 50
  ball_height = 20
  x_speed = 5  # Adjust for desired horizontal speed
  y_speed = 60  # Adjust for desired vertical speed
  running = True
  rect_initialized = False
  clock = pygame.time.Clock()  # Create a clock object

  # Additional rectangle for mouse tracking
  paddle_width = 200  # Adjust width of gray rectangle
  paddle_height = 20
  # Paddle start position
  paddle_x = 0
  paddle_y = 400

  score = 0  # Initialize score to 0
  score_display_active = False  # Flag to track score display visibility
  score_display_time = 0  # Timer for score display duration

  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False

    # Get delta time (time elapsed since last frame)
    delta_time = clock.tick(60) / 1000  # Get time in seconds

    # Screen fill (optional)
    screen.fill((0, 0, 0))

    if not rect_initialized:
      ball_y = 100  # Initialize on first iteration only
      rect_initialized = True

    # Update ball position and handle collisions (call handle_ball_movement only once)
    ball_x, ball_y, x_speed, y_speed = handle_ball_movement(ball_x, ball_y, ball_width, ball_height, x_speed, y_speed, delta_time, first_iteration)
    y_speed = handle_collisions(ball_x, ball_y, ball_width, ball_height, paddle_x, paddle_y, paddle_width, y_speed)

    # Update paddle position
    mouse_x, _ = pygame.mouse.get_pos()  # Only need x-coordinate
    paddle_x, paddle_y = handle_paddle_movement(paddle_x, paddle_y, paddle_width, mouse_x)

    # Draw objects on screen
    draw_objects(ball_x, ball_y, ball_width, ball_height, paddle_x, paddle_y, paddle_width, paddle_height)

    # Update score display timer
    score_display_time += delta_time

    # Deactivate score display if fade-out timer elapses
    if score_display_time > 1:  # Adjust fade-out duration (higher = longer fade)
      score_display_active = False

    pygame.display.flip()

    await asyncio.sleep(0)

  pygame.quit()

asyncio.run(main())
