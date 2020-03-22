import pygame
from pygame.transform import scale2x
import neat
import time
import os
import random

WIN_HEIGHT = 800
WIN_WIDTH = 500

BIRD_IMGS = []
for i in range(1, 4):
    img = pygame.image.load(os.path.join("imgs", f"bird{i}.png"))
    BIRD_IMGS.append(scale2x(img))
BG_IMG = scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
PIPE_IMG = scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = scale2x(pygame.image.load(os.path.join("imgs", "base.png")))


class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2
        if d >= 16:
            d = 16
        if d < 0:
            d -= 2

        self.y = self.y + d
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count >= self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        rot_img = pygame.transform.rotate(self.img, self.tilt)
        mid = self.img.get_rect(topleft=(self.x, self.y)).center
        rot_rect = rot_img.get_rect(center=mid)
        win.blit(rot_img, rot_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


def draw_window(win, bird):
    win.blit(BG_IMG, (0, 0))
    bird.draw(win)
    pygame.display.update()


def main():
    bird = Bird(200, 200)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clk = pygame.time.Clock()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        bird.move()
        draw_window(win, bird)
        clk.tick(30)
    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
