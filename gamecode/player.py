from config import *

class Player(pygame.sprite.Sprite):
    def __init__ (self, pos, groups):
        self.image = pygame.image.load(os.path.join(BASE_DIR, 'data', 'images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
