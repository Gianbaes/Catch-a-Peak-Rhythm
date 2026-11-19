from config import *
import time
from player import Player
import random

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

        self.notekeys = [
            pygame.K_w,
            pygame.K_e,
            pygame.K_d,
            pygame.K_s,
            pygame.K_a,
            pygame.K_q
        ]

        self.note_list = []

        for i in range(3):

            self.note_list.append({"x" : WINDOW_WIDTH - 500 + (i * 50), 
                                   "y" : 100 - (i * 50), 
                                   "requiredKey" : random.choice(self.notekeys),
                                     "noteclicked" : False,
                                     "noteIN" : False})
            self.noteindex = 0

            self.requiredKey = self.note_list[self.noteindex]

        self.prespawn =  False

        self.hike_x = 0
        self.hike_y = 0

        self.climbing = False
        self.Hike = False
        self.HikeSpeed = 350

        self.noteclicks = 0

        self.notetarget_x = WINDOW_WIDTH//2  -50
        self.notetarget_y = WINDOW_HEIGHT//2 - 85
        self.notetarget_area = 25

        self.notespeed = 75
        

        self.note = pygame.Rect(0,0, 30, 30)
        

        self.player = Player((WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 100), [])

        self.bg = pygame.image.load(os.path.join( 'data', 'images', 'bg.png')).convert_alpha()
        self.bg = pygame.transform.scale(self.bg,(WINDOW_WIDTH, WINDOW_HEIGHT))

        self.mountain = pygame.image.load(os.path.join( 'data', 'images', 'mountain.png')).convert_alpha()
        self.mountain = pygame.transform.scale(self.mountain,(WINDOW_WIDTH * 3, WINDOW_HEIGHT * 5 ))

        self.running = True

        self.note_spawn()




        self.display_surface.fill("Black")

    def note_reset (self):
        

        self.notespeed = 75

        self.note_list = [
            note for note in self.note_list
            if not note["noteclicked"]
        ]

        self.noteclicks += 1

        if self.noteclicks == 3:
            self.note_spawn()
            self.noteclicks = 0


        #self.noteindex += 1

    def note_spawn (self):
        self.note_list = []

        for i in range (3) :
            self.note_list.append({"x" : WINDOW_WIDTH - 550 + (i * 100), 
                                               "y" : 135 - (i * 100), 
                                               "requiredKey" : random.choice(self.notekeys),
                                                 "noteclicked" : False,
                                                 "noteIN" : False})  
        
        
    def notes(self, dt):   

        for note in self.note_list: 
            if not note["noteclicked"]:
                note["x"] -= self.notespeed * dt
                note["y"] += self.notespeed * dt
      
            notepos = pygame.math.Vector2(int(note["x"]), int(note["y"]))
            notetarget = pygame.math.Vector2(self.notetarget_x, self.notetarget_y)
            newnotepos = pygame.math.Vector2(self.notetarget_x, self.notetarget_y)
            min_d = 25

            distance = notepos.distance_to(notetarget)

            if distance <= min_d :
                note["noteIN"] = True
            else :
                note["noteIN"] = False

            if any(note["noteIN"] for note in self.note_list):
                color = "Green"
            else:
                color = "red"

                

            pygame.draw.circle(self.display_surface, "blue",
                                (int(note["x"]), int(note["y"])), 15)

            font = pygame.font.Font(None, 45)
            keytext = font.render( pygame.key.name(note["requiredKey"]).upper(), True, "White")

            self.display_surface.blit(keytext, ( int(note["x"] - 13 ), int(note["y"] - 13)))

        pygame.draw.circle(self.display_surface, color, (self.notetarget_x, self.notetarget_y), 15)

    def run (self):
        

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                
                    for note in self.note_list:
                        if event.key == note["requiredKey"]: 

                                if note["noteIN"] and not note["noteclicked"] and not self.climbing:
                                        note["noteclicked"] = True
                                        self.climbing = True
                                        self.note_reset()
                                        

                    
                    if self.climbing:
                        #self.targetpos_y = self.hike_y - 20
                        #self.targetpos_x = self.hike_x + 17
                        self.targetpos_y = self.hike_y - 40
                        self.targetpos_x = self.hike_x + 40
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
                    self.Hike = False

                    
                    

                self.mountain_y = -(WINDOW_HEIGHT* 4) - 350 -self.hike_y
                self.mountain_x = -(WINDOW_WIDTH * 2) + 2300 -self.hike_x


            pygame.display.update()

    pygame.quit() 
