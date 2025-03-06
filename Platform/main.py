import pygame


pygame.init()
width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

maxY = height



class character:
    def __init__(self, x, y, width, height, colour):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)

        self.width = width
        self.height = height
        self.maxY = 720
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
        
        self.colour = colour

        self.jump = 0
        self.grounded = False

    def update(self):
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
        pygame.draw.rect(screen, self.colour, self.rect)


player = character(0, 0, 50, 80, "blue")
platform = [character(0, 700, width/2, 20, "black"), character(width/2 + 75, 650, width/2, 20, "black")]

print(platform)



def main():
    while running:

        dt = clock.tick(60)
        screen.fill("purple")


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


        controller()

        collision()
        player.update()
        for p in platform:
            p.update()

        pygame.display.flip()


def controller():
    keys = pygame.key.get_pressed()

    speed = 3
    maxSpeed = 7
    friction = 2

    gravity = 2.5

    if keys[pygame.K_a]:
        player.vel.x -= speed
    if keys[pygame.K_d]:
        player.vel.x += speed

    if keys[pygame.K_SPACE] and player.grounded:
        player.vel.y = -30

    player.pos.y += player.vel.y
    player.vel.y += gravity

    player.pos.x += player.vel.x
    if player.vel.x < 0:
        player.vel.x += friction
    elif player.vel.x > 0:
        player.vel.x -= friction

    player.vel.x = max(min(player.vel.x, maxSpeed), -maxSpeed)

    player.pos.x = max(min(player.pos.x, width - player.width), 0)

def collision():
    plat_rect = []
    for i in platform:
        plat_rect.append(i.rect)

    plat_index = player.rect.collidelist(plat_rect)

    if plat_index != -1:
        player.maxY = platform[plat_index].rect.top
        player.vel.y = 0
        player.grounded = True
    else:
        player.maxY = height
        player.grounded = False
    player.pos.y = max(min(player.pos.y, player.maxY - player.rect.height), 0)


main()