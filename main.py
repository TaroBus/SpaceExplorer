import pygame
import random
from spaceship import Spaceship, Health, Projectile
from pygame import mixer
from meteor import Meteor
from start import Start

# Initialize Pygame
pygame.init()
mixer.init()
pygame.font.init()

# Get screen dimensions
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Space exploration!")

# Load assets
bg = pygame.image.load("Screen Assets/space.png").convert()
bg = pygame.transform.scale(bg, (screen_width, screen_height))

end_screen = pygame.image.load("Screen Assets/game-over.png").convert()
end_screen = pygame.transform.scale(end_screen, (screen_width, screen_height))

# mixer sounds
pygame.mixer.music.load("Sounds/Waterflame - Sky Fortress.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

laser = pygame.mixer.Sound("Sounds/laser.mp3")
explosion = pygame.mixer.Sound("Sounds/explosion.mp3")
explosion.set_volume(0.5)
collision1 = pygame.mixer.Sound("Sounds/collision1.mp3")
collision2 = pygame.mixer.Sound("Sounds/collision2.mp3")
collision3 = pygame.mixer.Sound("Sounds/collision3.mp3")
collision1.set_volume(0.3)
collision2.set_volume(0.3)
collision3.set_volume(0.3)
ship_boom = pygame.mixer.Sound("Sounds/ship_boom.mp3")
ship_boom.set_volume(0.3)

# Initialize clock and font
clocked = pygame.time.Clock()
my_font = pygame.font.SysFont("Inter", 48)
meteor_max = 20
current_meteors = 0

# Create spaceship, meteor, and projectile
s = Spaceship(100, screen_height // 2 - 100)
h = Health(0, 35)
m = Meteor(50, 50)
p = Projectile(s)

# Create sprite groups
projectile_list = pygame.sprite.Group()
meteor_list = pygame.sprite.Group()

# Set up game variables
play = True
firing = False
last_shot_time = 0
fire_rate = 200
score = 0
high_score = 0
health = 5
scoring = my_font.render(f"Current Score: {score}", True, (241, 250, 238))
end_score = my_font.render(f"HIGH SCORE!: {high_score}", True, (241, 250, 238))

# get username
name = Start(screen).run()
user_name = my_font.render(f"Username: {name}", True, (241, 250, 238))

while True:
    # create meteors
    if current_meteors < meteor_max:
        x = random.randint(screen_width // 4, screen_width - m.rect.width)
        y = random.randint(0, screen_height - m.rect.height)
        meteor_list.add(Meteor(x, y))
        current_meteors += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit()
            if event.key == pygame.K_SPACE and play:
                laser.play()
                firing = True
        if event.type == pygame.KEYUP and play:
            if event.key == pygame.K_SPACE:
                firing = False
    if play:
        # movement
        s.rotate()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            s.move_direction("d")
        if keys[pygame.K_a]:
            s.move_direction("a")
        if keys[pygame.K_w]:
            s.move_direction("w")
        if keys[pygame.K_s]:
            s.move_direction("s")

        # hit-box stuff
        collision_rect = s.mask.get_bounding_rects()[0]
        collision_rect.x += s.x
        collision_rect.y += s.y

        # Keep the spaceship within screen boundaries
        s.x = max(0, min(s.x, screen_width - collision_rect.width))
        s.y = max(0, min(s.y, screen_height - collision_rect.height - 45))

        # blit background
        screen.blit(bg, (0, 0))

        # creation of the projectiles
        if firing:
            current_time = pygame.time.get_ticks()
            if current_time - last_shot_time > fire_rate:
                p = Projectile(s)
                projectile_list.add(p)
                last_shot_time = current_time
        # update and check collisions
        projectile_list.update(False)
        for projectile in projectile_list:
            screen.blit(projectile.image, projectile.rect)
            if pygame.sprite.spritecollide(projectile, meteor_list, True, pygame.sprite.collide_mask):
                score += 1
                scoring = my_font.render(f"Current Score: {score}", True, (241, 250, 238))
                explosion.play()
                screen.blit(scoring, (0, h.rect[0] + 120))
                current_meteors -= 1
                p.update(True)
        # check collisions of the meteors and player
        if pygame.sprite.spritecollide(s, meteor_list, True, pygame.sprite.collide_mask):
            current_meteors -= 1
            play = h.damage()
            collide_num = random.randint(1, 3)
            health -= 1
            if health != 0:
                if collide_num == 1:
                    collision1.play()
                elif collide_num == 2:
                    collision2.play()
                else:
                    collision3.play()
            else:
                ship_boom.play()
        meteor_list.update()
        for meteor in meteor_list:
            screen.blit(meteor.image, meteor.rect)

        # blit stuff
        screen.blit(user_name, (0, 0))
        screen.blit(h.bar, h.rect)
        screen.blit(scoring, (0, h.rect[0] + 120))
        screen.blit(s.image, s.rect)
        screen.blit(scoring, (screen_width, 0))

    if not play:
        pygame.mixer.music.stop()
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
        health = 5
        if score > high_score:
            high_score = score
            end_score = my_font.render(f"HIGH SCORE!: {high_score}", True, (241, 250, 238))
        screen.blit(end_screen, (0, 0))
        screen.blit(end_score, (screen_width // 2 - 120, screen_height // 2 + 20))
        # if you press enter it resets everything
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            current_meteors = 0
            s = Spaceship(100, screen_height // 2 - 100)
            h = Health(0, 30)
            m = Meteor(50, 50)
            p = Projectile(s)

            projectile_list = pygame.sprite.Group()
            meteor_list = pygame.sprite.Group()
            play = True
            firing = False
            last_shot_time = 0
            score = 0
            scoring = my_font.render(f"Current Score: {score}", True, (241, 250, 238))
            # get username
            name = Start(screen).run()
            user_name = my_font.render(f"Username: {name}", True, (241, 250, 238))
    pygame.display.update()
    clocked.tick(60)
