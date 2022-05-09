class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()     
        self.pos = vec(0,0)
        self.vel = vec(0,0)
 
        self.direction = random.randint(0,1) # 0 POUR DROITE, 1 POUR GAUCHE
        self.vel.x = random.randint(2,6) / 2  # RANDOM VELOCITY ENNEMI
 
        # POSITION INITIALE ENNEMI
        if self.direction == 0:
            self.pos.x = 0
            self.pos.y = 235
        if self.direction == 1:
            self.pos.x = 700
            self.pos.y = 235
 
 
      def move(self):
        # CHANGEMENT DE DIRECTION DE ENNEMI AVANT DE SORTIR ECRAN
        if self.pos.x >= (WIDTH-20):
              self.direction = 1
        elif self.pos.x <= 0:
              self.direction = 0
 
        # ACTUALISE LES POSITIONS AVEC LES NOUVELLES VALEURS 
        if self.direction == 0:
            self.pos.x += self.vel.x
        if self.direction == 1:
            self.pos.x -= self.vel.x
             
        self.rect.center = self.pos # MET A JOUR rect
                
      def update(self):
            # CHERCHE LA COLLISION AVEC LE PLAYER
            hits = pygame.sprite.spritecollide(self, Playergroup, False)
            #print("fff")
 
            if hits and player.attacking == True:
                  print("Enemy Killed")
                  self.kill()
 
            # SI COLLISION ET LE PLAYER ATTAQUE PAS, APPELLE LA FONCTION HIT            
            elif hits and player.attacking == False:
                  player.player_hit()
                   
      def render(self):
            # ENNEMI A L ECRAN
            displaysurface.blit(self.image, (self.pos.x, self.pos.y))
 
 