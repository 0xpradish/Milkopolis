import pygame
from random import choice

from random import randint
pygame.init()

fire_list = []

bg_music = pygame.mixer.Sound('music/music.mp3')
bg_music.set_volume(0.3)

fire_music = pygame.mixer.Sound('music/fire.mp3')
fire_music.set_volume(0.2)




class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(400, 300))
        self.jump_music = pygame.mixer.Sound('music/jump.mp3')
        self.jump_music.set_volume(0.1)
        print(self.rect.width, self.rect.height)
        fire_surface = pygame.image.load('graphics/fire.png').convert_alpha()
        fire_surface = pygame.transform.scale(fire_surface, (180, 180))
        self.fire_image = fire_surface
        self.space_pressed = False
        self.gravity = 0

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

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
            self.jump_music.play()
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

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
            if fire.x > 800:
                fire_list.remove(fire)

    def update(self):
        self.player_movement()
        self.apply_gravity()
        self.fire()
        self.animation_state()

        

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

bg_music.play(loops = -1)

pygame.time.set_timer(snail_timer,2000)

test_font = pygame.font.Font('font/Pixeltype.ttf', 30)
test_font2 = pygame.font.Font('font/Pixeltype.ttf', 60)

score = 0
global health
health = 10
milk = 3
game_status = False

def player_collision(health):
    for snail in snails.sprites():
        if player.sprite.rect.right >= snail.rect.left and pygame.sprite.collide_rect(player.sprite, snail):
            health -= 5
            snail.kill()
    return health


milk_image = pygame.image.load('graphics/milk.png')
milk_image = pygame.transform.scale(milk_image, (90,100))
milk_rect = milk_image.get_rect(center=(randint(30, 780), 0))

snow_image = pygame.image.load('graphics/snowball.png')
snow_image = pygame.transform.scale(snow_image, (300,130))

snow_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snow_timer, 300)
snow_list = []

milk_list = []


    

def milk_loop(score):
    global m_pressed     
    keys = pygame.key.get_pressed()
    if keys[pygame.K_m]  and not m_pressed and len(milk_list) < 1 and score >= 5:
        milk_rect = milk_image.get_rect(center=(randint(30, 780), 0))
        milk_list.append(milk_rect)
        score -= 5
        m_pressed = True
    elif not keys[pygame.K_m]:
        m_pressed = False

    for milk in milk_list:
        milk.y += 1



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

        if game_status:
            if event.type == snail_timer:
                snails.add(Snail(choice(['snail'])))

        if game_status:
            if event.type == snow_timer:
                snow_rect = snow_image.get_rect(center=(randint(30, 780), 0))
                snow_list.append(snow_rect)

        if health <= 0:
            game_status = False

        else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    game_status = True

        
            
            
             
    
    
    if  game_status:
        screen.blit(sky_surface,(0,0))
        
        screen.blit(ground_surface,(0,230))

        milk_loop(score)
        # milk_collision(score,health) 

        player.draw(screen)
        player.update()



        snails.draw(screen)
        snails.update()

    
        
        

        for fire in fire_list: 
            screen.blit(player.sprite.fire_image, fire)
            fire_music.play()

        for fire in fire_list:
            
            for snail in snails.sprites():
                right_side_rect = pygame.Rect(snail.rect.right+30, snail.rect.top, 20, 10)
                if fire.colliderect(right_side_rect): 
                    score += 1 
                    snail.kill()
                    fire_list.remove(fire)
                    break

        

        
        
        health = player_collision(health)

        for milk in milk_list:
                screen.blit(milk_image,milk)
                player_eyes_rect = pygame.Rect(player.sprite.rect.x + player.sprite.rect.width, player.sprite.rect.y + player.sprite.rect.height // 2 - 2    + 40, 10, 40)
                for milk in milk_list:
                    if player_eyes_rect.colliderect(milk):
                        milk_list.remove(milk) 
                        score -= 5
                        health += 5
                

        

        score_message = test_font.render(f'score: {score}',False,(64,64,64))
        score_message_rect = score_message.get_rect(center = (50,20))
        health_message = test_font.render(f'health: {health}',False,(64,64,64))
        health_message_rect = health_message.get_rect(center = (750,20))



        screen.blit(score_message,score_message_rect)
        screen.blit(health_message,health_message_rect)

        snow_screen()
    
    elif game_status == False:
        screen.fill("#4c7087")

        milk_image = pygame.image.load('graphics/milk.png')
        milk_image = pygame.transform.scale(milk_image, (90,100))
        milk_rect = milk_image.get_rect(center=(300,190))
        milk_rect2 = milk_image.get_rect(center=(494,190))
        screen.blit(milk_image,milk_rect)
        screen.blit(milk_image,milk_rect2)
        display_message = test_font2.render("milkoPolis",False,"black")
        display_message_rect = display_message.get_rect(center = (400,200))

        score_message = test_font.render(f"You're score: {score}",False,"black")
        score_message_rect = score_message.get_rect(center = (400,250))

        press_p = test_font.render("Press P to start the game",False,"black")
        press_p_rect = press_p.get_rect(center = (400,300))
        
        
        keys = pygame.key.get_pressed()
        
        
        screen.blit(display_message,display_message_rect)
        screen.blit(score_message,score_message_rect)
        screen.blit(press_p,press_p_rect)
        
    pygame.display.update()
    clock.tick(60)
    