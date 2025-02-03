import pygame


pygame.init()
width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True


class character:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, "blue", self.rect)

player = character(0, 500, 50, 80)


def main():
    while running:
        dt = clock.tick()/1000
        screen.fill("purple")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


        controller(player, dt)
        player.update()

        pygame.display.flip()

        print(player.x, player.y)


def controller(player, dt):
    keys = pygame.key.get_pressed()
    speed = 300 * dt


    if keys[pygame.K_a]:
        player.x -= speed
    if keys[pygame.K_d]:
        player.x += speed
    if keys[pygame.K_w]:
        player.y -= speed
    if keys[pygame.K_s]:
        player.y += speed

    if keys[pygame.K_SPACE] and player.y == 420:
        player.y -= 100

    player.y += 0.2

    player.x = max(0, min(player.x, width - player.width))
    player.y = max(0, min(player.y, height - player.height - (height - 500)))

    return player


main()