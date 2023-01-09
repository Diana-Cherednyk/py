import pygame
import random 
from os import listdir
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT #константи числа

pygame.init()

FPS=pygame.time.Clock()

screen=width, heigth= 800, 600
#print(screen)# this is collection(tuple) it is unchanged
BLACK=0,0,0
RED=255,0,0
WHITE=255,255,255
YELLOW=255, 255, 0

font=pygame.font.SysFont("Verdana", 30)

main_surface=pygame.display.set_mode(screen)

IMGS_PATH = 'D:\py\Game\goose' 
# ball=pygame.Surface((20, 20))
# ball.fill(RED)
player_images = [pygame.transform.scale(pygame.image.load(IMGS_PATH + '/' + file).convert_alpha(), (101, 48)) for file in listdir(IMGS_PATH)]
#ball =pygame.transform.scale(pygame.image.load('D:\py\Game\player.png').convert_alpha(), (101, 48))                                                                                                                                                                                                                                                                                                                                     
ball=player_images[0]
ball_rect=ball.get_rect()
ball_speed=5
#ball_speed=[1,1]#changeable collection

def create_enemy():
    # enemy=pygame.Surface((20, 20))
    # enemy.fill(WHITE)
    enemy = pygame.transform.scale(pygame.image.load('Game/enemy.png').convert_alpha(), (92, 26) )
    enemy_rect=pygame.Rect(width, random.randint(10, heigth-10), *enemy.get_size())
    enemy_speed=random.randint(2,5)
    return [enemy, enemy_rect, enemy_speed]

CREATE_ENEMY=pygame.USEREVENT+1
pygame.time.set_timer(CREATE_ENEMY, 1500)
enemies=[]

def create_bonus():
    # bonus=pygame.Surface((20, 20))
    # bonus.fill(YELLOW)
    bonus = pygame.transform.scale(pygame.image.load('Game/bonus.png').convert_alpha(), (60,100))
    bonus_rect=pygame.Rect( random.randint(10, width-10), 0, *bonus.get_size())
    bonus_speed=random.randint(2,5)
    return [bonus, bonus_rect, bonus_speed]

bg =pygame.transform.scale(pygame.image.load('Game/g.png').convert(), screen)
bgX=0
bgX2=bg.get_width()
bg_speed=3


CREATE_BONUS=pygame.USEREVENT+2
pygame.time.set_timer(CREATE_BONUS, 1500)
bonuses=[]

CHANGE_IMG=pygame.USEREVENT+3
pygame.time.set_timer(CHANGE_IMG, 125)
img_index = 0
scores=0
is_working=True

while is_working:

    FPS.tick(60)#syn

    for event in pygame.event.get():
        if event.type==QUIT:
            is_working=False
        if event.type==CREATE_ENEMY:
            enemies.append(create_enemy())
            #pygame.quit() викликається прграмою?
        if event.type==CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type==CHANGE_IMG:
            img_index += 1
            if img_index == len(player_images):
                img_index=0
            ball=player_images[img_index]
    
    pressed_keys=pygame.key.get_pressed()
    #main_surface.fill(BLACK)
    #main_surface.blit(bg, (0, 0))
    bgX -= bg_speed
    bgX2 -= bg_speed
    if bgX < -bg.get_width():
        bgX = bg.get_width()

    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()
    
    main_surface.blit(bg, (bgX,0))
    main_surface.blit(bg, (bgX2,0))
    
    main_surface.blit(ball,(ball_rect))#змінюємо координати для перемальовування м'яча
    main_surface.blit(font.render(str(scores), True, BLACK), (width-60, 0))
    for enemy in enemies:
        enemy[1]=enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])

        if enemy[1].left<0:
            enemies.pop(enemies.index(enemy))
        
        if ball_rect.colliderect(enemy[1]):
            is_working=False
            #enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        bonus[1]=bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1])

        if bonus[1].bottom>heigth:
            bonuses.pop(bonuses.index(bonus))

        if ball_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            scores += 1
        

    if pressed_keys[K_DOWN] and not ball_rect.bottom>=heigth:
        ball_rect=ball_rect.move(0, ball_speed)
    if pressed_keys[K_UP] and not ball_rect.top<=0:
        ball_rect=ball_rect.move(0, -ball_speed)
    if pressed_keys[K_RIGHT] and not ball_rect.right>=width:
        ball_rect=ball_rect.move(ball_speed, 0)
    if pressed_keys[K_LEFT] and not ball_rect.left<=0:
        ball_rect=ball_rect.move( -ball_speed, 0)

    pygame.display.flip()#update our screen  

    # r=random.randint(10,255)
    # g=random.randint(10,255)
    # b=random.randint(10,255)
    # rgb=[r,g,b]
    # if ball_rect.bottom>=heigth or ball_rect.top<=0:
    #    ball_speed[1]=-ball_speed[1]
    #    ball.fill(rgb)
    # if ball_rect.right>=width or ball_rect.left<=0:  
    #    ball_speed[0]=-ball_speed[0]
    #    ball.fill(rgb)  
   # main_surface.fill((155,250,150))

   