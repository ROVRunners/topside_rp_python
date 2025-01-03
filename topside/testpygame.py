import pygame

pygame.init()

window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Controller")

controller = pygame.joystick.Joystick(0)

done = False

while not done:
    if controller.get_button(0): #A
        pygame.draw.rect(window, (255, 0, 0), [0, 0, 800, 600])
    if controller.get_button(1): #B
        pygame.draw.rect(window, (0, 255, 0), [0, 0, 800, 600])
    if controller.get_button(2): #X
        pygame.draw.rect(window, (0, 0, 255), [0, 0, 800, 600])
    if controller.get_button(3): #Y
        pygame.draw.rect(window, (0, 0, 0), [0, 0, 800, 600])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    pygame.display.update()

pygame.quit()
