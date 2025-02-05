import pygame


pygame.init()
width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True


class character:
    def __init__(self, x, y, width, height):
        self.pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.width = width
        self.height = height

    def update(self):
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
        pygame.draw.rect(screen, "blue", self.rect)

player = character(0, 500, 50, 80)


def main():
    while running:
        dt = clock.tick()/1000
        screen.fill("purple")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                print("Hit")


        controller(dt)
        player.update()

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

    if keydown() == True and player.pos.y == 420:
        player.velocity.y = -6

    player.velocity.y += 0.1
    player.pos.y += player.velocity.y

    player.pos.x = max(0, min(player.pos.x, width - player.width))
    player.pos.y = max(0, min(player.pos.y, height - player.height - (height - 500)))

def keydown():
    for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                print("Hit")
                return True
            else:
                return False



main()