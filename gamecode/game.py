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

        self.hike_x = 0
        self.hike_y = 0

        self.climbing = False
        self.Hike = False
        self.HikeSpeed = 350

        self.player = Player((WINDOW_WIDTH//2, WINDOW_HEIGHT//2), [])

        self.bg = pygame.image.load(os.path.join( 'data', 'images', 'bg.png')).convert_alpha()
        self.bg = pygame.transform.scale(self.bg,(WINDOW_WIDTH, WINDOW_HEIGHT))

        self.mountain = pygame.image.load(os.path.join( 'data', 'images', 'mountain.png')).convert_alpha()
        self.mountain = pygame.transform.scale(self.mountain,(WINDOW_WIDTH , WINDOW_HEIGHT))

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
                            self.targetpos += self.hike_y + 50
                            self.Hike = True
            

            

            self.display_surface.blit(self.bg, (0,0))
            self.display_surface.blit(self.mountain, (self.mountain_x, self.mountain_y))
            self.display_surface.blit(self.player.image, self.player.rect)

            dt = self.clock.tick(60)/ 1000

            if self.Hike:
                self.hike_x += self.HikeSpeed * dt 
                self.hike_y -= self.HikeSpeed * dt * 0.5

                
                

                if self.hike_y <= self.targetpos and self.hike_x >= self.targetpos:
                    self.hike_y = self.targetpos
                    self.hike_x = self.targetpos
                    self.climbing = False

            self.mountain_y = self.hike_y
            self.mountain_x = -self.hike_x


            pygame.display.update()

    pygame.quit() 
