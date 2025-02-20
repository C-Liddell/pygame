import pygame


pygame.init()
width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True



class character:
    def __init__(self, x, y, width, height, colour, grounded):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)
        self.acc = pygame.Vector2(0, 0)

        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
        
        self.colour = colour

        self.jump = 0
        self.grounded = grounded

    def update(self):
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
        pygame.draw.rect(screen, self.colour, self.rect)


player = character(0, 0, 50, 80, "blue", False)



def main():
    while running:

        dt = clock.tick(30)
        screen.fill("purple")


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


        controller()

        player.update()

        pygame.display.flip()


def controller():
    keys = pygame.key.get_pressed()
    speed = 10

    gravity = 6

    if keys[pygame.K_a]:
        player.pos.x -= speed
    if keys[pygame.K_d]:
        player.pos.x += speed

    if keys[pygame.K_SPACE] and player.grounded:
        player.jump += 15

    if player.pos.y == height - player.height:
        player.grounded = True
    else:
        player.pos.y += gravity
        player.grounded = False


    player.pos.y -= player.jump

    player.jump -= 3
    player.jump = max(0, player.jump)


    player.pos.x = max(min(player.pos.x, width - player.width), 0)
    player.pos.y = max(min(player.pos.y, height - player.height), 0)


main()