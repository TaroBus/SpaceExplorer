import pygame
import math
import os

pygame.init()
# screen info
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
screen_rect = pygame.Rect(0, 0, screen_width, screen_height)


# spaceship class
class Spaceship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.original_image = pygame.image.load("Screen Assets/redship4.png").convert_alpha()
        self.image_size = self.original_image.get_size()
        self.image = self.original_image
        # better hit box and save copy of original image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = pygame.Rect(self.x, self.y, self.image_size[0], self.image_size[1])
        self.delta = 5
        self.angle = 0
        self.health = 5

    # deal with rotation with trig :D
    def rotate(self):
        mouse_pos = pygame.mouse.get_pos()
        img_center = self.rect.center
        x_dist = mouse_pos[0] - img_center[0]
        y_dist = mouse_pos[1] - img_center[1]
        self.angle = math.degrees(math.atan2(y_dist, x_dist))
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=img_center)

    # move across the screen
    def move_direction(self, direction):
        if direction == "d":
            self.x = min(self.x + self.delta, screen_width - self.image_size[0])
        elif direction == "a":
            self.x = max(self.x - self.delta, 0)
        if direction == "w":
            self.y = max(self.y - self.delta, 0)
        elif direction == "s":
            self.y = min(self.y + self.delta, screen_height - self.image_size[1] - 15)
        self.rect = pygame.Rect(self.x, self.y, self.image_size[0], self.image_size[1])
        self.rect = self.image.get_rect(center=self.rect.center)


# health bar
class Health:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 5
        # loads a new image for each bar of health
        self.bar = pygame.image.load(os.path.join("Health", f"bar {self.health}.png")).convert_alpha()
        self.bar = pygame.transform.scale(self.bar, (740, 84))
        self.image_size = self.bar.get_size()
        self.rect = pygame.Rect(self.x, self.y, self.image_size[0], self.image_size[1])

    def damage(self):
        self.health -= 1
        if self.health < 1:
            return False
        self.bar = pygame.image.load(os.path.join("Health", f"bar {self.health}.png")).convert_alpha()
        self.bar = pygame.transform.scale(self.bar, (740, 84))
        self.image_size = self.bar.get_size()
        self.rect = pygame.Rect(self.x, self.y, self.image_size[0], self.image_size[1])
        return True


# laser class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, ship):
        super().__init__()
        # rect
        self.original_image = pygame.image.load("Screen Assets/laserBlue01.png").convert_alpha()
        self.rect = ship.rect.copy()
        self.rect.centerx = ship.rect.centerx + 50
        self.rect.y = ship.rect.y + 50
        # deals with angle
        self.angle = ship.angle
        self.image = pygame.transform.rotate(self.original_image, -self.angle - 90)
        # better hit box
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 8

    def update(self, hit):
        # to move in a certain direction when rotated
        self.rect.x += math.cos(math.radians(self.angle)) * self.speed
        self.rect.y += math.sin(math.radians(self.angle)) * self.speed
        # remove itself from the Group if out of bounds or hit
        if not screen_rect.colliderect(self.rect) or hit:
            self.kill()
