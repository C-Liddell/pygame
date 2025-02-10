import pygame


pygame.init()
width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True


class character:
    def __init__(self, x, y, width, height, colour):
        self.pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.width = width
        self.height = height
        self.colour = colour
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
        self.grounded = False

    def update(self):
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
        pygame.draw.rect(screen, self.colour, self.rect)


class platform:
    def __init__(self, x, y, width, height, colour):
        self.pos = pygame.Vector2(x, y)
        self.width = width
        self.height = height
        self.colour = colour
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)

    def update(self):
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
        pygame.draw.rect(screen, self.colour, self.rect)

player = character(0, 0, 50, 80, "blue")

platforms = platform(0, 420, width, 300, "black")


def main():
    while running:

        dt = clock.tick()/1000
        screen.fill("purple")


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and player.grounded == True:
                player.velocity.y = -6


        controller(dt)
        player.update()

        platforms.update()


        pygame.display.flip()


def controller(dt):
    keys = pygame.key.get_pressed()
    speed = 300 * dt


    if keys[pygame.K_a]:
        player.pos.x -= speed
    if keys[pygame.K_d]:
        player.pos.x += speed
    if keys[pygame.K_w]:
        player.pos.y -= speed
    if keys[pygame.K_s]:
        player.pos.y += speed

    if player.grounded == False:
        player.velocity.y += 0.05
    player.pos.y += player.velocity.y


    if platforms.rect.colliderect(player.rect):
        player.pos.y = platforms.rect.top - player.height
        player.grounded = True
        print("Hit")
    else:
        player.grounded = False


    player.pos.x = max(0, min(player.pos.x, width - player.width))


main()