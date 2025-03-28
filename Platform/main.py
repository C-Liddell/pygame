import pygame
import csv


pygame.init()
width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True



class Character:
    def __init__(self, x, y):
        self.start_pos = pygame.Vector2(x, y)
        self.pos = pygame.Vector2(x, y)
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

    def reset(self):
        self.pos.x = self.start_pos.x
        self.pos.y = self.start_pos.y
        print(self.pos)



class Platform:
    def __init__(self, x, y, width, height, colour):
        self.pos = pygame.Vector2(x,y)
        self.width = width
        self.height = height

        self.colour = colour

        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)

    def update(self):
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
        pygame.draw.rect(screen, self.colour, self.rect)

def loadLevel(lvlNo):
    platform = []
    with open(f"Platform/level{lvlNo}.txt", "r") as file:
        data = csv.reader(file)
        player_pos = next(data)
        player = Character(int(player_pos[0]), int(player_pos[1]))
        finish_pos = next(data)
        finish = Platform(int(finish_pos[0]), int(finish_pos[1]), int(finish_pos[2]), int(finish_pos[3]), finish_pos[4])
        for lines in data:
            platform.append(Platform(int(lines[0]), int(lines[1]), int(lines[2]), int(lines[3]), lines[4]))
    return platform, player, finish
        


def main():
    levelCounter = 1
    platform, player, finish = loadLevel(levelCounter)
    while running:
        clock.tick(60)
        screen.fill("purple")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
        player = controller(player, platform)
        player.update()

        for p in platform:
            p.update()

        finish.update()

        if player.rect.colliderect(finish.rect):
            levelCounter += 1
            try:
                platform, player, finish = loadLevel(levelCounter)
            except:
                print("You win")
                pygame.quit()

        pygame.display.flip()



def controller(player, platform):
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
    player = collision(player, platform)
    return player



def collision(player, platform):
    plat_rect = [p.rect for p in platform]
    plat_index = player.rect.collidelist(plat_rect)

    if plat_index != -1:
        if player.rect.center[1] <= plat_rect[plat_index].top:
            player.maxY = platform[plat_index].rect.top
            player.grounded = True

        elif player.rect.center[1] > plat_rect[plat_index].bottom:
            player.minY = platform[plat_index].rect.bottom
        player.vel.y = 0

        if platform[plat_index].colour == "red":
            player.reset()

    elif plat_index == -1:
        player.maxY = height
        player.minY = 0
        player.grounded = False

        if player.rect.bottom >= height:
            player.reset()

    player.pos.y = max(min(player.pos.y, player.maxY - player.rect.height), player.minY)
    return player



main()