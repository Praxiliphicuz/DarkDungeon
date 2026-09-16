import pygame

pygame.init()

# -----------------------------
# GAME SETTINGS
# -----------------------------

WIDTH = 800
HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dark Dungeon")

clock = pygame.time.Clock()

# -----------------------------
# PLAYER IMAGE
# -----------------------------

player_image = pygame.image.load("assets/player.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (64, 64))

# -----------------------------
# PLAYER PORTRAIT
# -----------------------------

player_portrait = pygame.image.load("assets/player_portrait.png").convert_alpha()
player_portrait = pygame.transform.scale(player_portrait, (48, 64))

font = pygame.font.Font(None, 28)

# -----------------------------
# COLORS
# -----------------------------

BACKGROUND = (18, 14, 22)
WALL_COLOR = (55, 48, 62)
PLAYER_COLOR = (150, 120, 180)

# -----------------------------
# PLAYER
# -----------------------------

player_width = 32
player_height = 32

player = pygame.Rect(
    WIDTH // 2,
    HEIGHT // 2,
    player_width,
    player_height
)

player_speed = 4
player_health = 100
damage_cooldown = 1000
last_damage_time = 0

# -----------------------------
# DUNGEON WALLS
# -----------------------------

walls = [
    pygame.Rect(0, 0, WIDTH, 40),             # top wall
    pygame.Rect(0, HEIGHT - 40, WIDTH, 40),   # bottom wall
    pygame.Rect(0, 0, 40, HEIGHT),            # left wall
    pygame.Rect(WIDTH - 40, 0, 40, HEIGHT),   # right wall

    pygame.Rect(200, 150, 400, 30),           # inner wall
    pygame.Rect(200, 420, 400, 30),
]

# -----------------------------
# ENEMY
# -----------------------------

enemy = pygame.Rect(500, 300, 32, 32)
enemy_speed = 2
enemy_color = (120, 35, 45)

# -----------------------------
# MAIN GAME LOOP
# -----------------------------

running = True

while running:

    # -------------------------
    # EVENTS
    # -------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    # -------------------------
    # INPUT
    # -------------------------

    keys = pygame.key.get_pressed()

    dx = 0
    dy = 0

    if keys[pygame.K_w]:
        dy -= player_speed

    if keys[pygame.K_s]:
        dy += player_speed

    if keys[pygame.K_a]:
        dx -= player_speed

    if keys[pygame.K_d]:
        dx += player_speed

    # -------------------------
    # HORIZONTAL COLLISION
    # -------------------------

    player.x += dx

    for wall in walls:
        if player.colliderect(wall):

            if dx > 0:
                player.right = wall.left

            if dx < 0:
                player.left = wall.right

    # -------------------------
    # VERTICAL COLLISION
    # -------------------------

    player.y += dy

    for wall in walls:
        if player.colliderect(wall):

            if dy > 0:
                player.bottom = wall.top

            if dy < 0:
                player.top = wall.bottom


    # -----------------------------
    # ENEMY MOVEMENT
    # -----------------------------

    enemy_dx = 0
    enemy_dy = 0

    if enemy.x < player.x:
        enemy_dx = enemy_speed

    if enemy.x > player.x:
        enemy_dx = -enemy_speed

    if enemy.y < player.y:
        enemy_dy = enemy_speed

    if enemy.y > player.y:
        enemy_dy = -enemy_speed


    # -----------------------------
    # ENEMY HORIZONTAL COLLISION
    # -----------------------------

    enemy.x += enemy_dx

    for wall in walls:
            if enemy.colliderect(wall):

                if enemy_dx > 0:
                    enemy.right = wall.left

                if enemy_dx < 0:
                    enemy.left = wall.right


    # -----------------------------
    # ENEMY VERTICAL COLLISION
    # -----------------------------

    enemy.y += enemy_dy

    for wall in walls:
        if enemy.colliderect(wall):

            if enemy_dy > 0:
                enemy.bottom = wall.top

            if enemy_dy < 0:
                enemy.top = wall.bottom


    # -----------------------------
    # PLAYER DAMAGE
    # -----------------------------

    current_time = pygame.time.get_ticks()

    if enemy.colliderect(player):

        if current_time - last_damage_time >= damage_cooldown:

            player_health -= 10
            last_damage_time = current_time

            print("Player Health:", player_health)

    if player_health <= 0:
        running = False



    # -------------------------
    # DRAWING
    # -------------------------

    screen.fill(BACKGROUND)

    # Draw Walls

    for wall in walls:
        pygame.draw.rect(screen, WALL_COLOR, wall)

    # DRAW ENEMY

    pygame.draw.rect(screen, enemy_color, enemy)

    # DRAW PLAYER

    player_draw_rect = player_image.get_rect(center=player.center)
    screen.blit(player_image, player_draw_rect)


    # -----------------------------
    # PLAYER HUD
    # -----------------------------

    screen.blit(player_portrait, (15, 15))

    health_text = font.render(
        f"HP: {player_health}",
        True,
        (255, 255, 255)
    )

    screen.blit(health_text, (75, 18))

    health_bar_x = 75
    health_bar_y = 48
    health_bar_width = 180
    health_bar_height = 18

    # Health bar background
    pygame.draw.rect(
        screen,
        (60, 20, 20),
        (health_bar_x, health_bar_y, health_bar_width, health_bar_height)
    )

    # Calculate current health-bar width
    current_health_width = health_bar_width * (player_health / 100)

    # Draw current health
    pygame.draw.rect(
        screen,
        (170, 40, 50),
        (health_bar_x, health_bar_y, current_health_width, health_bar_height)
    )


    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()