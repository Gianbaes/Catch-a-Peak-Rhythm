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

        self.peak_rect = pygame.Rect( self.mountain_x + int(151 * 19.22) , self.mountain_y + (28 * 24) - 130,
                                      int(300 * 2), int(15 * 4)) 

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

        self.notespeed_addition = [
            5,5,5,
            10,10,
            15,
            20,
            35,
            40,
            -5,-5,-5,-5
            -10,-10,-10
            -15,
            -20
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

        self.distance_to_peak = 0
        self.max_distduration = 3205

        self.climbing = False
        self.Hike = False
        self.pause = False
        self.playerwon = False
        self.playerlose = False
        self.AllowMovement = True

        self.HikeSpeed = 350

        self.noteclicks = 0

        self.notetarget_x = WINDOW_WIDTH//2  -50
        self.notetarget_y = WINDOW_HEIGHT//2 - 85
        self.notetarget_area = 25

        self.notespeed_Centralized = 75
        

        self.note = pygame.Rect(0,0, 30, 30)
        

        self.player = Player((WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 100), [])

        self.bg = pygame.image.load(os.path.join( 'data', 'images', 'bg.png')).convert_alpha()
        self.bg = pygame.transform.scale(self.bg,(WINDOW_WIDTH, WINDOW_HEIGHT))

        self.winDOW = pygame.image.load(os.path.join( 'data', 'images', 'winDOW.png')).convert_alpha()
        self.winDOW = pygame.transform.scale(self.winDOW,(WINDOW_WIDTH, WINDOW_HEIGHT))

        self.loseDOW = pygame.image.load(os.path.join( 'data', 'images', 'loseDOW.png')).convert_alpha()
        self.loseDOW = pygame.transform.scale(self.loseDOW,(WINDOW_WIDTH, WINDOW_HEIGHT))

        self.midbg = pygame.image.load(os.path.join( 'data', 'images', 'midground.png')).convert_alpha()
        self.midbg = pygame.transform.scale(self.midbg,(WINDOW_WIDTH, WINDOW_HEIGHT // 2 + 400))
        
        self.mountain = pygame.image.load(os.path.join( 'data', 'images', 'mountain.png')).convert_alpha()
        self.mountain = pygame.transform.scale(self.mountain,(WINDOW_WIDTH * 3, WINDOW_HEIGHT  * 5 ))

        self.running = True

        self.note_spawn()

        self.display_surface.fill("Black")

    def note_reset (self):
        
        self.notespeed_Centralized += random.choice(self.notespeed_addition)

        if self.notespeed_Centralized < 75 and self.notespeed_Centralized > 50:
            self.notespeed_Centralized += 25
        if self.notespeed_Centralized > 200 and self.notespeed_Centralized < 250:
            self.notespeed_Centralized -= 75

        print(self.notespeed_Centralized)
        
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

        for i in range (4) :
            self.note_list.append({"x" : WINDOW_WIDTH - 550 + (i * 100), 
                                    "y" : 135 - (i * 100), 
                                    "requiredKey" : random.choice(self.notekeys),
                            
                                        "noteclicked" : False,
                                        "noteIN" : False})  
            
    def notes(self, dt):   

        for note in self.note_list: 

            if not self.pause and not self.playerwon:
                if not note["noteclicked"]:
                    note["x"] -= self.notespeed_Centralized * dt
                    note["y"] += self.notespeed_Centralized * dt
      
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

    def pausemenu (self):
        clicking = False

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                        clicking = True
                        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                        self.pause = False
                        self.AllowMovement = True
   
        self.ambience_dark = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        self.ambience_dark.fill ((0, 0, 0, 100))
        self.display_surface.blit(self.ambience_dark, (0,0))
    
        menupause = pygame.Rect(0, 0, 400, 550)
        menupause.center = (
                WINDOW_WIDTH // 2,
                WINDOW_HEIGHT // 2
        )

        pygame.draw.rect(self.display_surface,(15, 25, 60), menupause, border_radius = 20)

        mouse_X, mouse_Y = pygame.mouse.get_pos()
        
        font = pygame.font.Font(None, 100)
        return_text = font.render(f"Return", True, "white")
        return_rect = return_text.get_rect(center =
                                            (600,430)
                                    )

        font = pygame.font.Font(None, 100)
        reset_text = font.render(f"Reset", True, "white")
        reset_rect = reset_text.get_rect(center =
                                            (600,330)
                                    )

        font = pygame.font.Font(None, 90)
        resume_text = font.render(f"Resume", True, "white")
        resume_rect = return_text.get_rect(center =
                                            (600,230)
                                    )

        self.display_surface.blit(resume_text, resume_rect)
        self.display_surface.blit(return_text, return_rect)
        self.display_surface.blit(reset_text, reset_rect)

        mouse_alligned_resume = resume_rect.collidepoint((mouse_X, mouse_Y))
        mouse_alligned_return = return_rect.collidepoint((mouse_X, mouse_Y))
        mouse_alligned_reset = reset_rect.collidepoint((mouse_X, mouse_Y))

        if mouse_alligned_resume and clicking == True :
            self.pause = False
            self.AllowMovement = True

        if mouse_alligned_reset and clicking == True :
            self.__init__()
            self.pause = False
            self.AllowMovement = True


        if mouse_alligned_return and clicking == True  :
            self.running = False
            
    def playerWin (self):
        clicking = False
             

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicking = True

        window = pygame.image.load(os.path.join( 'data', 'images', 'winDOW.png')).convert()
        window = pygame.transform.scale(window, (1000, 500))

        mouse_X, mouse_Y = pygame.mouse.get_pos()
        
        self.display_surface.blit( window, (150,120))




        font = pygame.font.Font(None, 100)
        retry_text = font.render(f"Return", True, "yellow")
        retry_rect = retry_text.get_rect(center =
                                            (650,550)
                                    )

        self.display_surface.blit (retry_text, retry_rect)         
        
        mouse_alligned_return = retry_rect.collidepoint((mouse_X, mouse_Y)) 
                
        
        
        if mouse_alligned_return and clicking == True  :
            self.running = False
            self.AllowMovement = True

        pygame.display.update()

    def run (self):
        
  
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if self.AllowMovement:
                        if event.key == pygame.K_t: #for testing purposes to quickly climb
                            self.climbing = True

                    if event.key == pygame.K_SPACE:
                        self.pause = True

                    for note in self.note_list:
                        if self.AllowMovement :   
                            if event.key == note["requiredKey"]: 
                                    if note["noteIN"] and not note["noteclicked"] and not self.climbing:
                                            note["noteclicked"] = True
                                            self.climbing = True
                                            self.note_reset()
                                        
 
                    if self.climbing:
                        #self.targetpos_y = self.hike_y - 20
                        #self.targetpos_x = self.hike_x + 17

                        self.targetpos_y = self.hike_y - 40
                        self.targetpos_x = self.hike_x + 35
                        self.Hike = True
            
            dt = self.clock.tick(60)/ 1000
            

            self.display_surface.blit(self.bg, (0,0))
            self.display_surface.blit(self.midbg, (0, 0))
            self.display_surface.blit(self.mountain, (self.mountain_x, self.mountain_y))
            self.notes(dt) #where the notes is

            self.display_surface.blit(self.player.image, self.player.rect)



            player = pygame.math.Vector2(self.notetarget_x, self.notetarget_y)
            peaktarget = pygame.math.Vector2(self.mountain_x + int(151 * 19.22), self.mountain_y + (28 * 24) - 130 ) 
            
            self.distance_to_peak = player.distance_to(peaktarget)
            self.distance_to_peak = self.distance_to_peak - 400
            print(self.distance_to_peak)

            distbar_width =300
            distbar_height = 30
            fill_ratio = self.distance_to_peak / self.max_distduration
            fill_width = int(distbar_width * fill_ratio)


            distbar_bg_rect = pygame.Rect(500, 10, distbar_width, distbar_height)
            pygame.draw.rect(self.display_surface, (50, 50, 50), distbar_bg_rect, border_radius = 4)

            if fill_width > 0 :
                  fill_rect = pygame.Rect(500,10, fill_width, distbar_height)
                  pygame.draw.rect(self.display_surface, (0,191,255), fill_rect, border_radius = 4)

            pygame.draw.rect(self.display_surface, (255, 255, 255), distbar_bg_rect, width=2, border_radius=4)

            font = pygame.font.Font(None, 30)
            DistanceCounter = font.render(f"Mountain Peak:  {int(self.distance_to_peak)} meters ", True, "White")
            self.display_surface.blit(DistanceCounter,(520, 13))
            

            if self.pause:
                self.pausemenu()
                self.AllowMovement = False
            else:
                self.AllowMovement = True

            if self.player.rect.colliderect(self.peak_rect):
                self.playerwon = True

            if self.playerwon:
                self.playerWin()
                self.AllowMovement = False
            else:
                self.AllowMovement = True

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

                self.peak_rect.topleft =(
                    self.mountain_x + int(171 * 19.2) ,
                    self.mountain_y + int(28 * 24) - 130
                )

               

            
            pygame.display.update()
                   
    pygame.quit() 
    
