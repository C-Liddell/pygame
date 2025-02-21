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
        self.acc = pygame.Vector2(0, 0)

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

        dt = clock.tick(30)
        screen.fill("purple")


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


        controller()
        player.update()

        collision()
        for p in platform:
            p.update()

        pygame.display.flip()


def controller():
    keys = pygame.key.get_pressed()
    speed = 10
    gravity = 10

    if keys[pygame.K_a]:
        player.pos.x -= speed
    if keys[pygame.K_d]:
        player.pos.x += speed

    if keys[pygame.K_SPACE] and player.grounded:
        player.jump = 30

    
    player.pos.y += gravity

    player.pos.y -= player.jump

    player.jump -= 3
    player.jump = max(0, player.jump)


    player.pos.x = max(min(player.pos.x, width - player.width), 0)

def collision():
    plat_rect = []
    for i in platform:
        print(player.rect.bottom, i.rect.top)
        plat_rect.append(i.rect)

    plat_index = player.rect.collidelist(plat_rect)

    if plat_index != -1:
        player.maxY = platform[plat_index].rect.top
        player.grounded = True
    else:
        player.maxY = height
        player.grounded = False
    player.pos.y = max(min(player.pos.y, player.maxY - player.rect.height), 0)


main()