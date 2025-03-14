import pygame
import sys
import os
import random
import time
import math

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
    global ball_speed_x, ball_speed_y, player_score, player2_score, start, speed_multiplier, last_speed_increase_time

    # Move the ball with speed scaled by delta time and multiplier
    ball.x += ball_speed_x * dt * speed_multiplier
    ball.y += ball_speed_y * dt * speed_multiplier

    # --- SPEED INCREASE LOGIC ---
    current_time = time.time()
    # Increase speed every 20 seconds up to a maximum of 1.5x
    if current_time - last_speed_increase_time > 20 and speed_multiplier < 1.5:
        speed_multiplier += 0.005 / (1 + speed_multiplier)
        last_speed_increase_time = current_time

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
    global player_speed, speed_multiplier
    
    # Base speed for both player and CPU (identical for fairness)
    base_speed = 300
    
    # Apply the same speed scaling as the CPU
    current_speed = base_speed * (0.8 + (speed_multiplier * 0.2))
    
    # Move the player paddle
    player.y += player_speed * current_speed * dt
    
    # Keep paddle within screen boundaries
    if player.top <= 10:
        player.top = 10
    if player.bottom >= screen_height - 10:
        player.bottom = screen_height - 10

def cpu_movement(dt):
    """
    Handle CPU AI movement - exactly the same speed as player for fairness
    """
    global speed_multiplier
    
    # Base speed for both player and CPU (identical for fairness)
    base_speed = 300
    
    # Apply the same speed scaling as the player
    current_speed = base_speed * (0.8 + (speed_multiplier * 0.2))
    
    # Calculate where the ball will be when it reaches the CPU's side
    if ball_speed_x > 0:  # Only predict when ball is moving toward CPU
        # Simple prediction of ball's y-position when it reaches the paddle
        time_to_reach = (player2.x - ball.x) / (ball_speed_x * speed_multiplier) if ball_speed_x != 0 else 0
        predicted_y = ball.y + (ball_speed_y * speed_multiplier * time_to_reach)
        
        # Some randomization to make CPU imperfect (more human-like)
        # Higher difficulty reduces randomness
        randomness = 30 * (2.0 - speed_multiplier)
        target_y = predicted_y + random.uniform(-randomness, randomness)
        
        # Ensure target stays within screen bounds
        target_y = max(min(target_y, screen_height - player2.height/2 - 10), player2.height/2 + 10)
        
        # Move toward the predicted position at exactly the same speed capability as player
        if player2.centery < target_y:
            player2.y += current_speed * dt
        elif player2.centery > target_y:
            player2.y -= current_speed * dt
    else:
        # When ball is moving away, gradually return to center with some delay
        if abs(player2.centery - screen_height/2) > 50:
            if player2.centery < screen_height/2:
                player2.y += (current_speed * 0.5) * dt
            else:
                player2.y -= (current_speed * 0.5) * dt

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
    ball_speed_x, ball_speed_y = 0, 0  # Stop ball movement
    
    # Reset player and cpu positions
    player2.centery = ball.centery
    player.centery = ball.centery 
    
    start = False

def draw_menu():
    """
    Draw the main menu screen
    """
    # Draw title
    title_text = pygame.font.Font('freesansbold.ttf', 72).render('Paddle Panic', True, light_grey)
    title_rect = title_text.get_rect(center=(screen_width/2, screen_height/4))
    screen.blit(title_text, title_rect)
    
    # Draw menu options
    for i, option in enumerate(menu_options):
        # Selected option is brighter and larger
        if i == menu_selected_index:
            text = menu_large_font.render(option, True, (255, 255, 255))
        else:
            text = menu_small_font.render(option, True, light_grey)
        
        text_rect = text.get_rect(center=(screen_width/2, screen_height/2 + i * 70))
        screen.blit(text, text_rect)
    
    # Draw instruction
    instruction = menu_small_font.render('Press ENTER to select', True, light_grey)
    instruction_rect = instruction.get_rect(center=(screen_width/2, screen_height - 50))
    screen.blit(instruction, instruction_rect)
    
    # Draw ball at the position of the dot in "i"
    ball_pos = ((screen_width / 2) + 181, screen_height / 4 - 30)
    ball_radius = 10
    pygame.draw.circle(screen, ball_color, ball_pos, ball_radius)

def handle_menu_input(event):
    """
    Handle input specifically for the menu screen
    """
    global menu_selected_index, game_state
    
    match event.key:
        case pygame.K_UP:
            menu_selected_index = (menu_selected_index - 1) % len(menu_options)
            paddle_hit_sound.play()
        case pygame.K_DOWN:
            menu_selected_index = (menu_selected_index + 1) % len(menu_options)
            paddle_hit_sound.play()
        case pygame.K_RETURN:
            selected_option = menu_options[menu_selected_index]
            match selected_option:
                case "Start":
                    game_state = "PLAYING"
                    restart()
                case "Exit":
                    pygame.quit()
                    sys.exit()

def handle_input(event):
    """
    Process keyboard input - using match/case
    """
    global player_speed, start, ball_speed_x, ball_speed_y, game_state
    
    # Using match/case for efficient input handling
    match event.type:
        case pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        case pygame.KEYDOWN:
            # Menu state handling
            if game_state == "MENU":
                handle_menu_input(event)
            # Playing state handling
            elif game_state == "PLAYING":
                match event.key:
                    case pygame.K_UP:
                        player_speed -= 1  # Move paddle up
                    case pygame.K_DOWN:
                        player_speed += 1  # Move paddle down
                    case pygame.K_SPACE:
                        if not start:
                            start = True
                            ball_speed_x = 400 * random.choice((1, -1))  # Random horizontal direction
                            ball_speed_y = 400 * random.choice((1, -1))  # Random vertical direction
                    case pygame.K_ESCAPE:
                        game_state = "MENU"
                        start = False
                    
        case pygame.KEYUP:
            if game_state == "PLAYING":
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
ball_color = (170, 111, 115)
paddle_color1 = (102, 84, 94)
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
speed_multiplier = 1.0
last_speed_increase_time = time.time()


# Game state
game_state = "MENU"  # Can be "MENU" or "PLAYING"

# Menu variables
menu_options = ["Start", "Exit"]
menu_selected_index = 0
menu_large_font = pygame.font.Font('freesansbold.ttf', 48)
menu_small_font = pygame.font.Font('freesansbold.ttf', 28)

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

    # Clear screen
    screen.fill(bg_color)
    
    # Handle different game states
    if game_state == "MENU":
        draw_menu()
    elif game_state == "PLAYING":
        # Update game state with delta time
        ball_movement(dt)
        player_movement(dt)
        cpu_movement(dt)
        
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
        
        # Display game instructions
        if not start:
            instruction = pygame.font.Font('freesansbold.ttf', 20).render('Press SPACE to start', False, light_grey)
            screen.blit(instruction, (screen_width/2 - instruction.get_width()/2, screen_height - 50))
            
        # Display escape hint
        esc_hint = pygame.font.Font('freesansbold.ttf', 16).render('ESC for menu', False, light_grey)
        screen.blit(esc_hint, (10, 10))
    
    # Update display and maintain frame rate
    pygame.display.flip()
    clock.tick(60)