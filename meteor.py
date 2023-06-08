import pygame
import random
import os

pygame.init()
# screen info
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
screen_rect = pygame.Rect(0, 0, screen_width, screen_height - 50)
screen = pygame.display.set_mode((screen_width, screen_height - 50))


# meteor class
class Meteor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # to use pygame Sprite features
        super().__init__()
        # read through the folder and randomly select meteors to create
        meteor_images = []
        for file_name in os.listdir("Meteors"):
            image = pygame.image.load(os.path.join("Meteors", file_name)).convert_alpha()
            meteor_images.append(image)
        self.images = meteor_images
        self.image = random.choice(self.images)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = random.randint(1, 3)

    def update(self):
        # fixed flight to the right and reset
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.x = random.randint(screen_width, screen_width + 250)
            self.rect.y = random.randint(0, screen_height - self.rect.height)
            self.speed = random.randint(1, 3)
