waterbottle_height = random.randint(50, 300)
waterbottle_rotate = random.randint(0, 360)
waterbottle = pygame.transform.rotate(waterbottle, waterbottle_rotate)
waterbottle_x -= 5
screen.blit(waterbottle, (waterbottle_x, waterbottle_y))
pygame.display.flip()
pygame.display.update()
