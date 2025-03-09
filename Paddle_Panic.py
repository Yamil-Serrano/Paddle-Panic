import pygame
import sys
import os
import random
import time

def resource_path(relative_path):
    """ Getting the absolute resources path for pyinstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def ball_movement(dt):
    """
    Handle all ball movement and collision logic
    """
    global ball_speed_x, ball_speed_y, player_score, player2_score, start

    # Move the ball according to its speed, scaled by delta time
    ball.x += ball_speed_x * dt
    ball.y += ball_speed_y * dt

    # --- COLLISION DETECTION ---
    
    # Player paddle collision (left paddle)
    if ball.colliderect(player):
        if abs(ball.left - player.right) < 10 and ball_speed_x < 0:
            ball_speed_x *= -1  # Reverse horizontal 
            paddle_hit_sound.play()  # Play sound
            # Move ball outside collision zone
            ball.left = player.right + 11
            
    # Player2 paddle collision (right paddle)
    if ball.colliderect(player2):
        if abs(ball.right - player2.left) < 10 and ball_speed_x > 0:
            ball_speed_x *= -1  # Reverse horizontal direction
            paddle_hit_sound2.play()  # Play sound
            # Move ball outside collision
            ball.right = player2.left - 11

    # Top and bottom wall collisions
    if ball.top <= 0:
        ball.top = 0  # Prevent ball from going outside screen
        ball_speed_y *= -1  # Reverse vertical direction
        
    elif ball.bottom >= screen_height:
        ball.bottom = screen_height  # Prevent ball from going outside screen
        ball_speed_y *= -1  # Reverse vertical direction

    # Left and right boundaries (scoring)
    if ball.left <= 0:
        player2_score += 1  # CPU scores a point
        no_score_sound.play()
        restart()  # Reset game when ball goes out of bounds
    elif ball.right >= screen_width:
        player_score += 1  # Player scores a point
        score_sound.play()
        restart()  # Reset game when ball goes out of bounds

def player_movement(dt):
    """
    Handle player paddle movement
    """
    player_speed_pixels_per_second = player_speed * 300  # Convert to pixels per second
    player.y += player_speed_pixels_per_second * dt  # Scale by delta time

    # Keep paddle within screen boundaries
    if player.top <= 10:
        player.top = 10
    if player.bottom >= screen_height - 10:
        player.bottom = screen_height - 10

def cpu_movement(dt):
    """
    Handle CPU paddle movement - follows the ball
    """
    cpu_speed = 350  # Pixels per second
    
    # AI logic: CPU paddle follows ball position with limited speed
    if player2.centery < ball.centery:
        player2.y += cpu_speed * dt  # Move down, scaled by delta time
    elif player2.centery > ball.centery:
        player2.y -= cpu_speed * dt  # Move up, scaled by delta time

    # Keep paddle within screen boundaries
    if player2.top <= 10:
        player2.top = 10
    if player2.bottom >= screen_height - 10:
        player2.bottom = screen_height - 10

def draw_dashed_line():
    """
    Draw a dashed line in the middle of the screen
    """
    dash_length = 15
    gap_length = 10
    center_x = screen_width // 2
    
    # Draw dashed line segments from top to bottom
    for y in range(0, screen_height, dash_length + gap_length):
        pygame.draw.line(
            screen, 
            light_grey, 
            (center_x, y), 
            (center_x, y + dash_length), 
            3  # Line width
        )

def restart():
    """
    Reset ball position after scoring
    """
    global ball_speed_x, ball_speed_y, start
    ball.center = (screen_width / 2, screen_height / 2)  # Center the ball
    ball_speed_y, ball_speed_x = 0, 0  # Stop ball movement
    
    # Reset player and cpu positions
    player2.centery = ball.centery
    player.centery = ball.centery 
    
    start = False

def handle_input(event):
    """
    Process keyboard input - using match/case
    """
    global player_speed, start, ball_speed_x, ball_speed_y
    
    # Using match/case for efficient input handling
    match event.type:
        case pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        case pygame.KEYDOWN:
            match event.key:
                case pygame.K_UP:
                    player_speed -= 1  # Move paddle up
                case pygame.K_DOWN:
                    player_speed += 1  # Move paddle down
                case pygame.K_SPACE:
                    if not start:  # Solo permite iniciar el juego si no ha comenzado
                        start = True
                        ball_speed_x = 400 * random.choice((1, -1))  # Random horizontal direction
                        ball_speed_y = 400 * random.choice((1, -1))  # Random vertical direction
                    
        case pygame.KEYUP:
            match event.key:
                case pygame.K_UP:
                    player_speed += 1  # Stop moving up
                case pygame.K_DOWN:
                    player_speed -= 1  # Stop moving down

# --- GAME INITIALIZATION ---

# Initialize Pygame
pygame.mixer.pre_init(44100, -16, 1, 1024)
pygame.init()
clock = pygame.time.Clock()

# Display setup
screen_width = 700
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Paddle Panic')

# Colors 
light_grey = (200, 200, 200)
ball_color = (170,111,115)
paddle_color1 = (102,84,94)
bg_color = (174, 156, 157)

# Game objects
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)  # Ball
player = pygame.Rect(10, (screen_height / 2) - 60, 15, 120)  # Player paddle (left)
player2 = pygame.Rect(screen_width - 25, (screen_height / 2) - 60, 15, 120)  # CPU paddle (right)

# Load sound effects
paddle_hit_sound = pygame.mixer.Sound(resource_path("Audio/impactTin_medium_003.ogg"))  
paddle_hit_sound2 = pygame.mixer.Sound(resource_path("Audio/impactTin_medium_001.ogg"))
score_sound = pygame.mixer.Sound(resource_path("Audio/confirmation_001.ogg"))
no_score_sound = pygame.mixer.Sound(resource_path("Audio/error_003.ogg"))

# Game variables
ball_speed_x = 0
ball_speed_y = 0
player_speed = 0
player2_speed = 0
player_score = 0
player2_score = 0
start = False

# Font for score display
basic_font = pygame.font.Font('freesansbold.ttf', 32)

# Delta time variables
previous_time = time.time()

# --- MAIN GAME LOOP ---
while True:
    # Calculate delta time
    current_time = time.time()
    dt = current_time - previous_time
    previous_time = current_time
    
    # Cap delta time to prevent physics issues if game freezes
    dt = min(dt, 0.1)
    
    # Process events
    for event in pygame.event.get():
        handle_input(event)


    # Update game state with delta time
    ball_movement(dt)
    player_movement(dt)
    cpu_movement(dt)

    # Render graphics
    screen.fill(bg_color)
    
    # Draw middle dashed line
    draw_dashed_line()
    
    # Draw paddles with rounded corners
    pygame.draw.rect(screen, paddle_color1, player, border_radius=7)
    pygame.draw.rect(screen, paddle_color1, player2, border_radius=7)
    
    # Draw ball
    pygame.draw.ellipse(screen, ball_color, ball)
    
    # Display scores
    player_text = basic_font.render(f'{player_score}', False, light_grey)
    player2_text = basic_font.render(f'{player2_score}', False, light_grey)
    
    # Position scores on their respective sides
    screen.blit(player_text, (screen_width/4, 20))  # Left side
    screen.blit(player2_text, (3*screen_width/4, 20))  # Right side
    
    # Display FPS for debugging
    fps = int(clock.get_fps())
    fps_text = pygame.font.Font('freesansbold.ttf', 16).render(f'FPS: {fps}', False, light_grey)
    screen.blit(fps_text, (10, screen_height - 30))
    
    # Update display and maintain frame rate
    pygame.display.flip()
    clock.tick(60)  

    # if you wanna create a binary of the game, use this command in the terminal. Note: You need pyinstaller
    # pyinstaller --onefile --windowed --add-data "./Audio;Audio" --add-data "./icon;icon" --icon=./icon/ping-pong.ico Paddle_Panic.py