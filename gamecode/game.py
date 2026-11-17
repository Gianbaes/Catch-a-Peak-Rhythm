from config import *
import time
from player import Player

class PeakClimber:
    def __init__(self):

        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Catch_A_Peak_Rhythm")

        self.clock = pygame.time.Clock()


        self.mountain_y = 0
        self.mountain_x = 0
        self.targetpos = 0

        self.climbing = False
        self.Hike = False
        self.HikeSpeed = 350

        self.player = Player((WINDOW_WIDTH//2, WINDOW_HEIGHT//2), [])


        self.running = True


        self.display_surface.fill("Black")
        


    def run (self):
        

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e and not self.climbing:
                        self.climbing = True

                        if self.climbing:
                            self.targetpos += 50
                            self.Hike = True
            


            bg = pygame.image.load(os.path.join( 'data', 'images', 'bg.png')).convert_alpha()
            bg = pygame.transform.scale(bg,(WINDOW_WIDTH, WINDOW_HEIGHT))

            mountain = pygame.image.load(os.path.join( 'data', 'images', 'mountain.png')).convert_alpha()
            mountain = pygame.transform.scale(mountain,(WINDOW_WIDTH , WINDOW_HEIGHT))

            player = pygame.image.load(os.path.join( 'data', 'images', 'player.png')).convert_alpha()
            player = pygame.transform.scale(player,(WINDOW_WIDTH, WINDOW_HEIGHT)) 
            

            self.display_surface.blit(bg, (0,0))
            self.display_surface.blit(mountain, (self.mountain_x, self.mountain_y))
            self.display_surface.blit(self.player.image, self.player.rect)

            dt = self.clock.tick(60)/ 1000

            if self.Hike:
                self.mountain_y += self.HikeSpeed * dt 
                self.mountain_x -= self.HikeSpeed * dt 

                if self.mountain_y >= self.targetpos and self.mountain_x <= self.targetpos:
                    self.mountain_y = self.targetpos
                    self.mountain_x = self.targetpos
                    self.climbing = False


            pygame.display.update()

    pygame.quit() 
