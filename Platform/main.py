import pygame
import csv


pygame.init()
width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True



class Character:
    def __init__(self, pos):
        self.pos = pygame.Vector2(0, 0)
        self.maxY = 720
        self.minY = 0
        self.grounded = False

        self.vel = pygame.Vector2(0, 0)

        self.width = 50
        self.height = 80

        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)

        self.colour = "blue"

    def update(self):
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
        pygame.draw.rect(screen, self.colour, self.rect)


class Platform:
    colour = "black"
    def __init__(self, x, y, width, height):
        self.pos = pygame.Vector2(x,y)
        self.width = width
        self.height = height

        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)

    def update(self):
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
        pygame.draw.rect(screen, self.colour, self.rect)

def loadLevel(lvlNo):
    platform = []
    player = Character((0,0))
    with open(f"Platform/level{lvlNo}.txt", "r") as file:
        data = csv.reader(file)
        for lines in data:
            platform.append(Platform(int(lines[0]), int(lines[1]), int(lines[2]), int(lines[3])))
    return platform, player

        


def main():
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
        controller()

        screen.fill("purple")

        player.update()
        for p in platform:
            p.update()

        pygame.display.flip()



def controller():
    keys = pygame.key.get_pressed()

    acceleration = 2
    maxSpeed = 13
    friction = 1
    gravity = 2

    if keys[pygame.K_SPACE] and player.grounded:
        player.vel.y = -30
    if keys[pygame.K_a]:
        player.vel.x -= acceleration
    if keys[pygame.K_d]:
        player.vel.x += acceleration

    if player.vel.x < 0:
        player.vel.x += friction
    elif player.vel.x > 0:
        player.vel.x -= friction

    player.vel.x = max(min(player.vel.x, maxSpeed), -maxSpeed)
    player.pos.x += player.vel.x

    player.vel.y += gravity
    player.pos.y += player.vel.y

    player.pos.x = max(min(player.pos.x, width - player.width), 0)
    collision()



def collision():
    plat_rect = [p.rect for p in platform]
    plat_index = player.rect.collidelist(plat_rect)
    if plat_index != -1:
        if player.rect.center[1] <= plat_rect[plat_index].top:
            player.maxY = platform[plat_index].rect.top
            player.grounded = True
        if player.rect.center[1] > plat_rect[plat_index].bottom:
            player.minY = platform[plat_index].rect.bottom
        player.vel.y = 0
    elif plat_index == -1:
        player.maxY = height
        player.minY = 0
        player.grounded = False
    player.pos.y = max(min(player.pos.y, player.maxY - player.rect.height), player.minY)


platform, player = loadLevel(1)
main()