import pygame as pg
from pygame import mixer
import time
import math
import random

def scale_image(img_path):
    img=pg.image.load(img_path)
    scaled_img= pg.transform.scale(img, (int(img.get_width()/4), int(img.get_height()/4)))
    return scaled_img

background = scale_image('./assets/background.png')
score_widget= scale_image('./assets/score-widget.png')


WIDTH= int(background.get_width())
HEIGHT= int(background.get_height())
clock = pg.time.Clock()
dt = clock.tick(800)
score = 0
bones=[]
SPACE_BAR_PRESSED=0
mouse_click=0

pg.init()

window = pg.display.set_mode((WIDTH, HEIGHT))



class Bone:
    def __init__(self,img, width, height, x, y, dx, dy, relaxation_time):
        self.img=img
        self.width=width
        self.height=height
        self.x= x
        self.y=y
        self.dx= dx * dt
        self.dy= dy * dt
        self.relaxation_time = relaxation_time

    def draw(self):
        window.blit(self.img, (int(self.x), int(self.y)))

class Dog:
    def __init__(self, img, width, height, x, y, dx, dxb, dy, relaxation_time):
        self.img=img
        self.width=width
        self.height= height
        self.x= x
        self.y=y
        self.dx= dx * dt
        self.dxb = dxb *dt
        self.dy= dy * dt
        self.relaxation_time = relaxation_time
        self.clicked = False

    def draw(self):
        window.blit(self.img, (int(self.x), int(self.y)))


#Functions
def out_of_bounds(obj):
    y_bound= HEIGHT-score_widget.get_height() - (obj.height)
    if obj.y>y_bound:
        return True

def scoreboard():
    font = pg.font.SysFont("arial", 16)
    score_sprite = font.render(str(score), True, (0,0,0))
    text_rect = score_sprite.get_rect(center=(int(score_widget.get_width()/2), int(HEIGHT - (score_widget.get_height()/2))))

    window.blit(score_sprite, text_rect)

def collision_check(object1, object2):
    x1_cm = object1.x + object1.width / 2
    y1_cm = object1.y + object1.height / 2
    x2_cm = object2.x + object2.width / 2
    y2_cm = object2.y + object2.height / 2
    distance = math.sqrt(math.pow((x2_cm - x1_cm), 2) + math.pow((y2_cm - y1_cm), 2))
    return distance < ((object1.width + object2.width) / 2)


#initializing the game
def init_game():

    #Small Bone
    global small_bone
    small_bone_img= scale_image('./assets/small-bone.png')
    small_bone_width= small_bone_img.get_width()
    small_bone_height= small_bone_img.get_height()
    small_bone_x= (WIDTH / 2) - (small_bone_width / 2)
    small_bone_y= 0
    small_bone_dx= 1.0
    small_bone_dy=0.2
    small_bone_relaxation_time= 100
    small_bone=Bone(small_bone_img, small_bone_width, small_bone_height, small_bone_x, small_bone_y, small_bone_dx, small_bone_dy, small_bone_relaxation_time)


    global big_bone
    big_bone_img= scale_image('./assets/big-bone.png')
    big_bone_width= big_bone_img.get_width()
    big_bone_height= big_bone_img.get_height()
    big_bone_x= (WIDTH / 2) - (big_bone_width / 2)
    big_bone_y= 0
    big_bone_dx= 1.0
    big_bone_dy= 0.2
    big_bone_relaxation_time= 100
    big_bone=Bone(big_bone_img, big_bone_width, big_bone_height, big_bone_x, big_bone_y, big_bone_dx, big_bone_dy,big_bone_relaxation_time)

    #Small Dog
    global small_dog
    small_dog_img= scale_image('./assets/small-stick-dog.png')
    small_dog_width= small_dog_img.get_width()
    small_dog_height= small_dog_img.get_height()
    small_dog_x = -(small_dog_width) + 20
    small_dog_y= HEIGHT/2
    small_dog_dx= 0.5
    small_dog_dxb = 0.2
    small_dog_dy=0.2
    small_dog_relaxation_time= 100
    small_dog=Dog(small_dog_img, small_dog_width, small_dog_height, small_dog_x, small_dog_y, small_dog_dx, small_dog_dxb, small_dog_dy, small_dog_relaxation_time)

    #Big Dog
    global big_dog
    big_dog_img= scale_image('./assets/big-stick-dog.png')
    big_dog_width= big_dog_img.get_width()
    big_dog_height= big_dog_img.get_height()
    big_dog_x = WIDTH - 20
    big_dog_y= HEIGHT/2
    big_dog_dx= 0.5
    big_dog_dxb = 0.2
    big_dog_dy=0.2
    big_dog_relaxation_time= 100
    big_dog=Dog(big_dog_img, big_dog_width, big_dog_height, big_dog_x, big_dog_y, big_dog_dx, big_dog_dxb, big_dog_dy, big_dog_relaxation_time)

init_game()
# min_dist=big_bone.img.get_height()
running =True
small_dog_clicked=False
while running:
    if out_of_bounds(small_bone):
        running = False
        continue

    window.fill((0, 0, 0))
    window.blit(background,(0,0))
    window.blit(score_widget,(0,HEIGHT-score_widget.get_height()))
    small_bone.y += small_bone.dy
    small_bone.draw()
    small_dog.draw()
    big_dog.draw()
    scoreboard()
    

    for event in pg.event.get():
        if event.type==pg.QUIT:
            running=False
        
        if event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            if pos[0] <= (WIDTH/2 - small_bone.width/2): #for left side of screen
                if small_dog.x <= -(small_dog.width) + 20 and not small_dog.clicked:
                    small_dog.clicked=True

            if pos[0] >= (WIDTH/2 + small_bone.width/2): #for right side of screen
                if big_dog.x >= (big_dog.width) - 20 and not big_dog.clicked:
                    big_dog.clicked=True
                
    #Small Dog movement     
    if small_dog.clicked and (small_dog.x + small_dog.width) <(WIDTH/2 - small_bone.width/3) :
        small_dog.y = pos[1]-small_dog.height/2
        small_dog.x += small_dog.dx

    else:
        small_dog.clicked=False
    
    if not small_dog.clicked and small_dog.x > -(small_dog.width) + 20 :
        small_dog.x -= small_dog.dxb

    #Big Dog movement
    if big_dog.clicked and (big_dog.x) > (WIDTH/2 + small_bone.width/3) :
        big_dog.y = pos[1]-big_dog.height/2
        big_dog.x -= big_dog.dx

    else:
        big_dog.clicked=False
    
    if not big_dog.clicked and big_dog.x < WIDTH - 20 :
        big_dog.x += big_dog.dxb


    dog_eat_bone = collision_check(small_dog, small_bone) or collision_check(small_bone, big_dog)
    if dog_eat_bone:
        score += 1
        small_bone.y= 0
        scoreboard()

    pg.display.update()

    
    # keys = pg.key.get_pressed()
    # if keys[pg.K_SPACE]:
    #     small_dog.x = (small_dog.x + small_dog.img.get_width()) <(WIDTH/2 - small_bone.img.get_width()/2)
    #     space_press+=1
