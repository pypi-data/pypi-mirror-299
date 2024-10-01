import pygame_canvas as c

c.window(title = "game")

font = None
font = c.pygame.font.Font("mine.otf")

# sprite declaration here:
object = c.sprite((c.rectangle(50,50,(0,200,255)),),(240,180))
color = "black"


while c.loop(60, color):
    
    c.set_title(f"Real cumming game!!!   |   fps: {c.get_FPS()}")

    pass
