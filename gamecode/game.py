from config import *
import time

class PeakClimber:
    def __init__(self):

        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Catch_A_Peak_Rhythm")

        self.running = True

        self.display_surface.fill("Black")
        

    def run (self):
        

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            


            bg = pygame.image.load(os.path.join( 'data', 'images', 'bg.png')).convert_alpha()
            bg = pygame.transform.scale(bg,(WINDOW_WIDTH, WINDOW_HEIGHT))

            self.display_surface.blit(bg, (0,0))


            pygame.display.update()

    pygame.quit() 
