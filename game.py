import pygame
from random import choice

from random import randint
pygame.init()

fire_list = []
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.gravity = 0

        player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
        self.image = player_stand
        self.rect = self.image.get_rect(midbottom = (400,300))
        fire_surface = pygame.image.load('graphics/fire.png').convert_alpha()
        fire_surface = pygame.transform.scale(fire_surface, (180,180))
        self.fire_image = fire_surface
        self.space_pressed = False
        
    def player_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.left >= 2:
            self.rect.x -= 5
        elif keys[pygame.K_d] and self.rect.right < 798:
            self.rect.x += 5
        elif keys[pygame.K_w] and self.rect.bottom >= 300:
            self.gravity = -15
        elif keys[pygame.K_s] and self.rect.bottom >= 300:
             
             self.gravity = -20
    
    def apply_gravity(self):
            self.gravity += 1
            self.rect.y += self.gravity
            if self.rect.bottom >= 300:
                    self.rect.bottom = 300

    def fire(self):
         
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.space_pressed:
            self.fire_rect = self.fire_image.get_rect(center=(self.rect.x + self.rect.width, self.rect.y + 40 + self.rect.height // 2 - 2))
            fire_list.append(self.fire_rect)
            self.space_pressed = True  
        elif not keys[pygame.K_SPACE]:
            self.space_pressed = False 
        
        for fire in fire_list:
              fire.x += 7
              if fire.x > 800 :
                   fire_list.remove(fire)
    
    
         
         

    def update(self):
        self.player_movement()
        self.apply_gravity()
        self.fire()
        

class Snail(pygame.sprite.Sprite):
   
    def __init__(self,type):
        super().__init__()
        
        if type == 'snail':
             
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1,snail_2]

            self.animation_index = 0
            self.image = self.frames[self.animation_index]
            self.rect = self.image.get_rect(midbottom = (900,300))

    def animation_state(self):
         self.animation_index += 0.1
         if self.animation_index >= len(self.frames) : self.animation_index = 0
         self.image = self.frames[int(self.animation_index)]

    def update(self):
         self.animation_state()
         self.rect.x -= 3
         self.destroy()

    def destroy(self):
         if self.rect.x <= -100:
              self.kill()



screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('milK')
clock = pygame.time.Clock()

sky_surface = pygame.image.load('graphics/Sky.png').convert_alpha()
ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()

#Groups 
player = pygame.sprite.GroupSingle()
player.add(Player())

snails = pygame.sprite.Group()


snail_timer = pygame.USEREVENT + 1

pygame.time.set_timer(snail_timer,2000)

test_font = pygame.font.Font('font/Pixeltype.ttf', 30)

score = 0
global health
health = 30
milk = 3

def player_collision(health):
    for snail in snails.sprites():
        if player.sprite.rect.right >= snail.rect.left and pygame.sprite.collide_rect(player.sprite, snail):
            health -= 5
            snail.kill()
    return health


milk_image = pygame.image.load('graphics/milk.png')
milk_image = pygame.transform.scale(milk_image, (90,100))

snow_image = pygame.image.load('graphics/snowball.png')
snow_image = pygame.transform.scale(snow_image, (300,130))

snow_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snow_timer, 300)
snow_list = []

milk_list = []

def milk_loop():
    global m_pressed 

    
    keys = pygame.key.get_pressed()
    milk_rect = milk_image.get_rect(center=(randint(30, 780), 0))
    if keys[pygame.K_m] and not m_pressed:
        
        milk_list.append(milk_rect)
        m_pressed = True
    elif not keys[pygame.K_m]:
        m_pressed = False

    for milk in milk_list:
        milk.y += 1

        

def milk_collision():
    player_eyes_rect = pygame.Rect(player.sprite.rect.x + player.sprite.rect.width, player.sprite.rect.y + player.sprite.rect.height // 2 - 2    + 40, 10, 40)
    for milk in milk_list:
        if player_eyes_rect.colliderect(milk):
            milk_list.remove(milk) 
            
            


def snow_screen():
    for snow in snow_list:
        screen.blit(snow_image,snow)
        snow.y += 3
        if snow.y >= 300:
            snow_list.remove(snow)
    
    pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == snail_timer:
             snails.add(Snail(choice(['snail'])))

        if event.type == snow_timer:
            snow_rect = snow_image.get_rect(center=(randint(30, 780), 0))
            snow_list.append(snow_rect)
             
    
    

    screen.blit(sky_surface,(0,0))
    
    screen.blit(ground_surface,(0,230))

    milk_loop()
    milk_collision() 

    player.draw(screen)
    player.update()



    snails.draw(screen)
    snails.update()


    
    

    for fire in fire_list: 
        screen.blit(player.sprite.fire_image, fire)

    for fire in fire_list:
        
        for snail in snails.sprites():
            right_side_rect = pygame.Rect(snail.rect.right+30, snail.rect.top, 20, 10)
            if fire.colliderect(right_side_rect): 
                score += 1 
                snail.kill()
                fire_list.remove(fire)
                break

    

    for milk in milk_list:
        screen.blit(milk_image,milk)
    
    health = player_collision(health)

    

    

    score_message = test_font.render(f'score: {score}',False,(64,64,64))
    score_message_rect = score_message.get_rect(center = (50,20))
    health_message = test_font.render(f'health: {health}',False,(64,64,64))
    health_message_rect = health_message.get_rect(center = (750,20))

    

    

    screen.blit(score_message,score_message_rect)
    screen.blit(health_message,health_message_rect)

    snow_screen()

    pygame.display.update()
    clock.tick(60)
    