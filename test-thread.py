import threading
import pygame


def f():
    x = 80
    y = 80
    xd = 1
    yd = 1
    r = 20
    x1 = 300
    y1 = 300
    xd1 = 5
    yd1 = 5
    r1 = 30
    while True:
        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, (255, 0, 0, 255), (x, y), r)
        pygame.draw.circle(screen, (0, 0, 255, 255), (x1, y1), r1)
        pygame.display.flip()
        x = x + xd
        y = y + yd
        x1 = x1 + xd1
        y1 = y1 + yd1
        if x == (500-r) or x == r:
            xd = -xd
        if y == (400-r) or y == r:
            yd = -yd
        if x1 == (500-r1) or x1 == r1:
            xd1 = -xd1
        if y1 == (400-r1) or y1 == r1:
            yd1 = -yd1
        pygame.time.delay(10)

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((500, 400))
    t = threading.Thread(target=f)
    t.setDaemon(True)
    t.start()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.time.delay(100)

pygame.quit()