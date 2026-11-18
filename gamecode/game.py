from config import *
import time
from player import Player

class PeakClimber:
    def __init__(self):

        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Catch_A_Peak_Rhythm")

        self.clock = pygame.time.Clock()


        self.mountain_y = -(WINDOW_HEIGHT* 4) - 350
        self.mountain_x = -(WINDOW_WIDTH * 2) + 2300

        self.targetpos_x = 0
        self.targetpos_y = 0

        self.hike_x = 0
        self.hike_y = 0

        self.climbing = False
        self.Hike = False
        self.HikeSpeed = 350

        self.notetarget_x = WINDOW_WIDTH//2  -50
        self.notetarget_y = WINDOW_HEIGHT//2 - 85
        self.notetarget_area = 25

        self.note_x = WINDOW_WIDTH - 500
        self.note_y = 100
        self.notespeed = 250
        self.notemiss = False
        self.noteIN = False
        self.noteclicked = False

        self.note = pygame.Rect(0,0, 30, 30)
        

        self.player = Player((WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 100), [])

        self.bg = pygame.image.load(os.path.join( 'data', 'images', 'bg.png')).convert_alpha()
        self.bg = pygame.transform.scale(self.bg,(WINDOW_WIDTH, WINDOW_HEIGHT))

        self.mountain = pygame.image.load(os.path.join( 'data', 'images', 'mountain.png')).convert_alpha()
        self.mountain = pygame.transform.scale(self.mountain,(WINDOW_WIDTH * 3, WINDOW_HEIGHT * 5 ))

        self.running = True




        self.display_surface.fill("Black")
        
    def notes(self, dt):    

        self.note_x -= self.notespeed * dt
        self.note_y += self.notespeed * dt

        notepos = pygame.math.Vector2(self.note_x, self.note_y)
        notetarget = pygame.math.Vector2(self.notetarget_x, self.notetarget_y)
        newnotepos = pygame.math.Vector2(self.notetarget_x, self.notetarget_y)
        min_d = 25

        distance = notepos.distance_to(notetarget)

        if distance > min_d :
            self.noteIN = True
        else :
            self.noteIN = False

        if self.noteIN:
            color = "Green"
        else:
            color = "red"

            


        pygame.draw.circle(self.display_surface, color, (self.notetarget_x, self.notetarget_y), 15)

        pygame.draw.circle(self.display_surface, "Blue", (int(self.note_x), int(self.note_y)), 15)



    def run (self):
        

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w and not self.climbing:
                        self.climbing = True            



                    if event.key == pygame.K_e:
                            self.noteclicked = True                                  
                            if not self.noteIN and self.noteclicked:
                            
                                    self.climbing = True

                    
                if self.climbing:
                        self.targetpos_y = self.hike_y - 20
                        self.targetpos_x = self.hike_x + 17
                        self.Hike = True
            
            dt = self.clock.tick(60)/ 1000
            

            self.display_surface.blit(self.bg, (0,0))
            self.display_surface.blit(self.mountain, (self.mountain_x, self.mountain_y))
            self.notes(dt) #where the notes is
            self.display_surface.blit(self.player.image, self.player.rect)


            

            if self.Hike:
                self.hike_x += self.HikeSpeed * dt 
                self.hike_y -= self.HikeSpeed * dt * 0.5

                if self.hike_x >= self.targetpos_x:
                    self.hike_x = self.targetpos_x
                    self.hike_y = self.targetpos_y
                    self.climbing = False

                self.mountain_y = -(WINDOW_HEIGHT* 4) - 350 -self.hike_y
                self.mountain_x = -(WINDOW_WIDTH * 2) + 2300 -self.hike_x


            pygame.display.update()

    pygame.quit() 
