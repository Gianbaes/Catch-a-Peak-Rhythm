from config import *

class Player(pygame.sprite.Sprite):
    def __init__ (self, pos, groups):
        self.image = pygame.image.load(os.path.join( 'data', 'images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
