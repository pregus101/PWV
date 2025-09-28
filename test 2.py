import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

# The object to move
object_pos = [300, 200]
trail_points = []
trail_length = 30 # Number of points in the trail

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the state of all keyboard keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        object_pos[0] -= 5
    if keys[pygame.K_RIGHT]:
        object_pos[0] += 5
    if keys[pygame.K_UP]:
        object_pos[1] -= 5
    if keys[pygame.K_DOWN]:
        object_pos[1] += 5

    # Update the trail points list
    trail_points.insert(0, tuple(object_pos))
    if len(trail_points) > trail_length:
        trail_points.pop()

    screen.fill((0, 0, 0))

    # Draw the trail
    for i, point in enumerate(trail_points):
        # Scale the size of the trail effect based on its age
        size = 5 - int(i * 5 / trail_length)
        if size > 0:
            pygame.draw.circle(screen, (255, 255, 255), point, size)

    # Draw the main object
    pygame.draw.circle(screen, (255, 0, 0), object_pos, 10)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
