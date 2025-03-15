import pygame


pygame.init()
width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True



class Character:
    pos = pygame.Vector2(0, 0)
    maxY = 720
    grounded = False

    vel = pygame.Vector2(0, 0)

    width = 50
    height = 80

    rect = pygame.Rect

    colour = "blue"

    def update(self):
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
        pygame.draw.rect(screen, self.colour, self.rect)

player = Character()


class Platform:
    colour = "black"
    def __init__(self, x, y, width, height):
        self.pos = pygame.Vector2(x,y)
        self.width = width
        self.height = height

        self.rect = pygame.Rect

    def update(self):
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
        pygame.draw.rect(screen, self.colour, self.rect)

platform = [Platform(0, 700, width/2, 20), Platform(width/2 + 75, 650, width/2, 20)]



def main():
    while running:
        dt = clock.tick(60)
        screen.fill("purple")
        jump = False

        player.update()
        for p in platform:
            p.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                jump = True
            

        controller(jump)

        #print(player.grounded)

        pygame.display.flip()



def controller(jump):
    keys = pygame.key.get_pressed()

    acceleration = 2
    maxSpeed = 7
    friction = 1

    gravity = 2.5

    if keys[pygame.K_SPACE] and player.grounded:
        player.vel.y = -30

    player.pos.y += player.vel.y
    player.vel.y += gravity

    collision()


    if keys[pygame.K_a]:
        player.vel.x -= acceleration
    if keys[pygame.K_d]:
        player.vel.x += acceleration

    player.pos.x += player.vel.x
    if player.vel.x < 0:
        player.vel.x += friction
    elif player.vel.x > 0:
        player.vel.x -= friction

    player.vel.x = max(min(player.vel.x, maxSpeed), -maxSpeed)
    player.pos.x = max(min(player.pos.x, width - player.width), 0)



def collision():
    plat_rect = [p.rect for p in platform]
    plat_index = player.rect.collidelist(plat_rect)
    print(plat_index)
    if plat_index != -1:
        player.maxY = platform[plat_index].rect.top
        player.vel.y = 0
        player.grounded = True
    elif plat_index == -1:
        player.maxY = height
        player.grounded = False
    player.pos.y = max(min(player.pos.y, player.maxY - player.rect.height), 0)



main()