import pygame
import sys
import random
import math
import time



# 초기화
pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock() 

# 이미지 정의
cursor_image = pygame.image.load("ab.webp").convert_alpha()
cursor_image = pygame.transform.scale(cursor_image, ( 100, 80 ))
cursor1_image = pygame.image.load("HD_Repeater.webp").convert_alpha()
cursor1_image = pygame.transform.scale(cursor1_image, ( 80, 80 ))
flower_image = pygame.image.load("Sunflower2009HD.webp").convert_alpha()
flower_image = pygame.transform.scale(flower_image, ( 80, 80 ))
Chomper = pygame.image.load("Chomper-hd.webp").convert_alpha()
Chomper = pygame.transform.scale(Chomper, ( 90, 90 ))
Potato = pygame.image.load("potatomine.webp").convert_alpha()
Potato = pygame.transform.scale(Potato, ( 90, 70 ))
test_image = pygame.image.load("HDplus_gatling.webp").convert_alpha()
new_width = 100
aspect_ratio = test_image.get_width() / test_image.get_height()
new_height = int(new_width / aspect_ratio)
test_image = pygame.transform.scale(test_image, ( new_width, new_height ))
shovel_image = pygame.image.load("Shovel.png").convert_alpha()
shovel_image = pygame.transform.scale(shovel_image, ( 100, 100 ))
cursor_width, cursor_height = cursor_image.get_size()
# 색상 정의
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
aqua = (0, 255, 255)
BUZZER = (0, 0, 0)
# 사운드 정의
plant = pygame.mixer.Sound("SFX plant.mp3")
delete = pygame.mixer.Sound("SFX plant2.mp3")
SelectP = pygame.mixer.Sound("SFX seedlift.mp3")
shovel = pygame.mixer.Sound("SFX shovel.mp3")
shoot = pygame.mixer.Sound("SFX throw.mp3")
splat = pygame.mixer.Sound("SFX splat.mp3")
chomp = pygame.mixer.Sound("SFX chomp.mp3")
points = pygame.mixer.Sound("SFX points.mp3")
gulp = pygame.mixer.Sound("Voices gulp.mp3")
buzzer = pygame.mixer.Sound("SFX buzzer.mp3")
diggerzombie = pygame.mixer.Sound("SFX digger zombie.mp3")
bigchomp = pygame.mixer.Sound("SFX bigchomp.mp3")
PotatoMine = pygame.mixer.Sound("SFX potato mine.mp3")

# 폰트 정의
font = pygame.font.SysFont("arial", 30,  True, True)

map = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0]
       ]
box_size = 100
margin = 15
max_distance = 50

sunAmount = 0
sundownspeed = 2
# sunStartpos = -60
sunFire_rate = 5
sunLastTime = time.time()

# 깜빡임
blink_interval = 50
blink_count = 0
max_blinks = 4
blinking = False
last_blink_time = 0

suns = []
shots = []
zombies = []

# test
something = 0
fire_rate = 10
lasttime = time.time()


inv_width = 100
inv_height = 50
inv_margin = 20

inventory = [
    {
        "Name": "ME", 
        "Cost": 100,
        "hp": 600, 
        "damage": 200,
        "PlantRate": 4, 
        "LastRate": 0,
        "FireRate": 3,
        "PlantImage": cursor_image
    },
    {
        "Name": "MEa", 
        "Cost": 325, 
        "hp": 1000,
        "damage": 200, 
        "PlantRate": 0, 
        "LastRate": 0,
        "FireRate": 3, 
        "PlantImage": test_image
    },
    {
        "Name": "abbb", 
        "Cost": 200, 
        "hp": 900,
        "damage": 200, 
        "PlantRate": 0, 
        "LastRate": 0,
        "FireRate": 2, 
        "PlantImage": cursor1_image
    },
    {
        "Name": "flower", 
        "Cost": 50, 
        "hp": 1000,
        "damage": 200, 
        "PlantRate": 3, 
        "LastRate": 0,
        "FireRate": 30, 
        "PlantImage": flower_image
    },
    {
        "Name": "Chomper", 
        "Cost": 150, 
        "hp": 1000,
        "damage": 200, 
        "PlantRate": 0, 
        "LastRate": 0,
        "FireRate": 15, 
        "PlantImage": Chomper
    },
    {
        "Name": "Potato", 
        "Cost": 25, 
        "hp": 800,
        "damage": 1000000, 
        "PlantRate": 0, 
        "LastRate": 0,
        "FireRate": 8, 
        "PlantImage": Potato
    }
]
Selected= None

# Cost = 100
class Plant:
    def __init__(self, row, col, plant, hp = 50, fire_rate = 0.1):
        self.plant = plant
        self.row = row # test
        self.col = col # test
        self.x = self.row * (box_size + margin)
        self.y = self.col * (box_size + margin)
        self.max_hp = plant["hp"]
        self.hp = plant["hp"]
        self.Damage = plant["damage"]
        self.image = plant["PlantImage"] # Demo
        self.rect = pygame.Rect(self.x + 10, self.y + 10, 80, 80)
        
        self.fire_rate = plant["FireRate"]  # 발사 간격 (초 단위)
        self.last_shot_time = time.time()  # 마지막 발사 시간

        self.shot = 0
        self.last_shot = time.time()

    def draw(self, SCREEN, box_size, margin):
        # print(self.row, self.col)
        SCREEN.blit(self.image, (self.x, self.y))
    def debug(self, SCREEN, box_size, margin):
        pygame.draw.rect(SCREEN, aqua, self.rect)
    def Showhp(self, SCREEN):
        pygame.draw.rect(SCREEN, (255, 0, 0), (self.x + 5, self.y -5, box_size - 10, 10))

        health_ratio = self.hp / self.max_hp
        health_width = int((box_size -10) * health_ratio)

        pygame.draw.rect(SCREEN, (0, 255, 0), (self.x + 5, self.y -5, health_width, 10))
        

    def update(self, shots):
        # 현재 시간이 마지막 발사 시간에서 발사 간격을 더한 값보다 크면 발사
        if time.time() - self.last_shot_time >= self.fire_rate:
            if self.plant["Name"] == "MEa":
                fire_rate = 0.1
                if time.time() - self.last_shot >= fire_rate:
                    shots.append(Shot(self.x+ 50, self.y + 10, "pea", self.Damage))
                    self.last_shot = time.time()
                    self.shot += 1
                    if self.shot == 4:
                        # print("a")
                        self.last_shot_time = time.time()  # 발사 시간 업데이트
                        self.shot = 0
            elif self.plant["Name"] == "abbb":
                fire_rate = 0.1
                if time.time() - self.last_shot >= fire_rate:
                    shots.append(Shot(self.x+ 50, self.y + 10, "pea", self.Damage))
                    self.last_shot = time.time()
                    self.shot += 1
                    if self.shot == 2:
                        # print("a")
                        self.last_shot_time = time.time()  # 발사 시간 업데이트
                        self.shot = 0
            elif self.plant["Name"] == "flower":
                suns.append(Sun(self.x - 10, self.y + 50, 25, False))
                self.last_shot_time = time.time()
            elif self.plant["Name"] == "Chomper":
                for zombie in zombies[:]:
                    if zombie.x - self.x <= 100 and zombie.y == self.y: # y는 나중에 수정
                        zombies.remove(zombie)
                        bigchomp.play()
                self.last_shot_time = time.time()
            elif self.plant["Name"] == "Potato":
                for zombie in zombies[:]:
                    if zombie.x - self.x <= 90 and zombie.y == self.y: # y는 나중에 수정
                        zombies.remove(zombie)
                        PotatoMine.play()
                        map[self.col][self.row] = 0
                
            else:
                shots.append(Shot(self.x+ 90, self.y + 10, "pea", self.Damage))
                self.last_shot_time = time.time()  # 발사 시간 업데이트

            # print("발")
    def damage(self, damage):
        self.hp -= damage
        chomp.play()


class Shot:
    def __init__(self, x, y, type, damage):
        self.x = x
        self.y = y
        self.type = type
        self.speed = 10
        self.damage = damage # Demo
        self.rect = pygame.Rect(self.x, self.y, 20, 20)

        shoot.play()

    def draw(self, SCREEN):
        pygame.draw.rect(SCREEN, ( 0, 0, 255 ), self.rect)
        # print("엥")
    def move(self):
        self.x += self.speed
        self.rect = pygame.Rect(self.x, self.y, 20, 20)

        # print("위윙")

class Zombie:
    def __init__(self, x, col, hp, type, fire_rate=0.3, spawn_delay=1.5):
        self.x = x
        self.col = col
        self.y = self.col * (100 + margin)
        
        self.type = type
        self.speed = 1
        self.hp = hp 
        self.max_hp = hp
        self.power = 50 # damage
        self.rect = pygame.Rect(self.x, self.y, 50, 100)

        self.fire_rate = fire_rate  # 공격 간격 (초 단위)
        self.last_atk_time = time.time()  # 마지막 공격 시간

        #스폰 쿨타임
        self.spawn_delay = spawn_delay
        self.created_time = time.time()
        self.is_active = False


    def draw(self, SCREEN):
        if self.is_active:
            pygame.draw.rect(SCREEN, ( 0, 0, 255 ), self.rect)
    def Showhp(self, SCREEN):
        pygame.draw.rect(SCREEN, (255, 0, 0), (self.x - 20, self.y -5, box_size - 10, 10))

        health_ratio = self.hp / self.max_hp
        health_width = int((box_size -10) * health_ratio)

        pygame.draw.rect(SCREEN, (0, 255, 0), (self.x - 20, self.y -5, health_width, 10))


    def move(self):
        if self.is_active:
            self.x -= self.speed
            self.rect = pygame.Rect(self.x, self.y, 50, 100)
    def damage(self, damage):
        if self.is_active:
            self.hp -= damage
            splat.play()
    def attack(self, plant):
        if self.is_active:
            if time.time() - self.last_atk_time >= self.fire_rate:
                plant.damage(self.power)
                self.last_atk_time = time.time()  # 공격 시간 업데이트
            self.x += self.speed
            self.rect = pygame.Rect(self.x, self.y, 50, 100)
    def update(self):
        if not self.is_active and time.time() - self.created_time >= self.spawn_delay:
            self.is_active = True
class Sun:
    def __init__(self, x, y, SunAmount, auto=True):
        # print("윙")
        self.x = x
        self.SunAmount = SunAmount
        self.SunSize = self.SunAmount * 2
        
        self.auto = auto
        if auto==True:
            self.dy = y
            self.y = -self.SunSize
        else:
            self.y = y

        self.rect = pygame.Rect(self.x, self.y, self.SunSize, self.SunSize)
    def SunDown(self):
        # print("발")
        if self.auto == True:
            self.y += sundownspeed
            self.rect = pygame.Rect(self.x, self.y, self.SunSize, self.SunSize)

    def draw(self, SCREEN):
        pygame.draw.rect(SCREEN, ( 255, 255, 0 ), self.rect)
        


class Inventory:
    def __init__(self, x, y, width, height, plant):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.plant = plant
        self.Cost = plant["Cost"]
        self.PlantRate = plant["PlantRate"]

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    def update(self, SCREEN, LastRate):
        pygame.draw.rect(SCREEN, ( 0, 0, 255 ), self.rect)


        current_time = time.time()
        if current_time - LastRate < self.PlantRate:
            print(current_time, current_time - LastRate, self.PlantRate)
            Rate_ratio = ( time.time() - LastRate ) / self.PlantRate
            Rate_height = self.height -int(self.height * Rate_ratio)

            pygame.draw.rect(SCREEN, ( 0, 255, 0 ), (self.x, self.y, self.width, Rate_height))

test_a = Inventory(100, 500, inv_width, inv_height, inventory[3])


# 게임 루프
running = True
while running:
    current_time = pygame.time.get_ticks()
    mouse_x, mouse_y = pygame.mouse.get_pos()




    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # 사용자가 스페이스 키를 눌렀을 때
                if Selected== None:
                    Selected= "shovel"
                    shovel.play()
                else:
                    Selected= None
            if pygame.K_0 <= event.key <= pygame.K_9:
                key = event.key - pygame.K_0
                if len(inventory) - 1 < key:
                    key = 0
                if sunAmount >= inventory[key]["Cost"]:
                    if time.time() - inventory[key]["LastRate"] >= inventory[key]["PlantRate"]:
                        Selected= inventory[key]
                        SelectP.play()
                    else:
                        buzzer.play()
                else:
                    buzzer.play()
                    blinking = True
                    blink_count = key
                    last_blink_time = current_time

            if event.key == pygame.K_UP:
                if closest_box:
                    col = int(closest_box[1] / (box_size + margin))
                    diggerzombie.play()
                    # zombies.append(Zombie(1100, col, 500, "Normal", 1))
                    for i in range(6): # 6줄 동시에
                        zombies.append(Zombie(1100, i, 1000, "Normal", 1))


            if event.key == pygame.K_DOWN:
                sunAmount += 100

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (Selected == None):
                for sun in suns[:]:
                    if sun.rect.collidepoint(mouse_x, mouse_y):
                        points.play()
                        sunAmount += sun.SunAmount
                        suns.remove(sun)
            
            if (test_a.rect.collidepoint(mouse_x, mouse_y)):
                print("오 정재헌씨, 정답입니다.")

            if closest_box and min_distance <= max_distance:
                row =  int(closest_box[0] / (box_size + margin))
                col = int(closest_box[1] / (box_size + margin))
                print(row, col)
                if (Selected!= "shovel" and Selected) and map[col][row] == 0: # 나중에는 아마 선택시에 버저 울리게 할듯
                    # print(Selected)
                    map[col][row] = Plant(row, col, Selected)
                    Selected["LastRate"] = time.time()
                    plant.play()
                    sunAmount -= Selected["Cost"]
                    
                    Selected= None
                elif Selected== "shovel" and not(map[col][row] == 0):
                    map[col][row] = 0
                    delete.play()
            

                 
            
    # 화면 업데이트
    screen.fill((255, 255, 255))  # 화면을 흰색으로 채웁니다.
    

    # 가장 가까운 상자 찾기
    closest_box = None
    min_distance = float('inf')

    for col in range(len(map)):
        for row in range(len(map[col])):
            # 상자의 좌표 계산
            x = row * (box_size + margin)
            y = col * (box_size + margin)

            # 상자 중심점 계산
            center_x = x + box_size // 2
            center_y = y + box_size // 2

            # 마우스와 상자 중심 간의 거리 계산
            distance = math.sqrt((mouse_x - center_x) ** 2 + (mouse_y - center_y) ** 2)

            # 가장 가까운 상자 업데이트
            if distance < min_distance:
                min_distance = distance
                closest_box = (x, y)

    # 상자 그리기
    for col in range(len(map)):
        for row in range(len(map[col])):
            x = row * (box_size + margin)
            y = col * (box_size + margin)

            if closest_box == (x, y) and min_distance <= max_distance:
                if (Selected!= "shovel" and Selected):
                    if map[col][row] == 0:
                        color = red  # 가장 가까운 상자 중에서 일정 거리 이내인 경우 빨간색으로 표시
                elif not(map[col][row] == 0):
                    color = blue
            else:
                color = black  # 나머지 상자는 검은색

            pygame.draw.rect(screen, black, (x, y, box_size, box_size))
            if (Selected!= "shovel" and Selected) and closest_box== (x, y) and min_distance <= max_distance and map[col][row] == 0:
                cursor_image_copy = Selected["PlantImage"].copy()  # 이미지를 복사
                cursor_image_copy.set_alpha(100)  # 복사본에 투명도 적용

                screen.blit(cursor_image_copy, (x, y))

                #screen.blit(cursor_image_copy, (x, y))

            elif not(map[col][row] == 0):
                map[col][row].draw(screen, box_size, margin)
                map[col][row].Showhp(screen)
                # map[col][row].debug(screen, box_size, margin)
                map[col][row].update(shots)

                for zombie in zombies[:]:
                    try:
                        if zombie.rect.colliderect(map[col][row].rect):
                            print("zombie atk")
                            zombie.attack(map[col][row])
                            
                            if map[col][row].hp <=0:
                                map[col][row] = 0
                                gulp.play()
                                break
                    except Exception as e:
                        print(e)

    
    # 움직임 + 화면 이탈
    for shot in shots[:]: # [:]은 리스트를 복제함
        if shot.x >= 1280:
            shots.remove(shot)
        shot.move()
        shot.draw(screen)
        
        
    for zombie in zombies[:]:
        if zombie.x <= 0 or zombie.hp <= 0:
            zombies.remove(zombie)

        zombie.update()
        
        zombie.move()
        zombie.draw(screen)
        zombie.Showhp(screen)

    for sun in suns[:]:
        if sun.auto == True:
            if sun.dy > sun.y:
                sun.SunDown()
        sun.draw(screen)
            
    
    #태양 생성
    if time.time() - sunLastTime >= sunFire_rate:
        sunLastTime = time.time()
        suns.append(Sun(random.randint(0, WIDTH), 600, 25))
    
    # test
    if time.time() - lasttime >= fire_rate:
        something += 1
        lasttime = time.time()
        zombies.append(Zombie(1300, (random.randint(0, 5)), (random.randint(1200, 2300)), "Zombie", 2))
        if something == 17:
            fire_rate = random.randint(1, 20)
            something = 0
            diggerzombie.play()
            # zombies.append(Zombie(1100, col, 500, "Normal", 1))
            for i in range(6): # 6줄 동시에
                zombies.append(Zombie(1300, i, (random.randint(1900, 5000)), "Normal", 1))

    # #inventory
    # for plants in inventory:



    # 탄알이 좀비한테 맞았나
    for shot in shots[:]:
        for zombie in zombies[:]:
            if shot.rect.colliderect(zombie.rect) and zombie.is_active == True:
                print("atk")
                shots.remove(shot)
                zombie.damage(shot.damage)
                break

    # print(shots)
    # 커스텀 커서 이미지 그리기         
    x, y = pygame.mouse.get_pos()
    cursor_x = x - cursor_width // 2
    cursor_y = y - cursor_height // 2
    if (Selected!= "shovel" and Selected):
        screen.blit(Selected["PlantImage"], (cursor_x, cursor_y))
    elif Selected== "shovel":
        screen.blit(shovel_image, (cursor_x, cursor_y))

    # 깜빡임
    if blinking and current_time - last_blink_time >= blink_interval:
        blink_count += 1
        last_blink_time = current_time
        if (blink_count % 2 == 0):
            BUZZER = black
        else:
            BUZZER = red

        if blink_count >= max_blinks:
            BUZZER = black
            blinking = False
    
    #인벤토리 표시
    test_a.update(screen, inventory[3]["LastRate"])

    #Text 표시
    Text = font.render(f"Sun: {sunAmount}", True, BUZZER)
    screen.blit(Text, (1150, 0))

    pygame.display.flip()  # 화면을 업데이트합니다.
    clock.tick(60)  # FPS를 60으로 설정합니다.

pygame.quit()
sys.exit()