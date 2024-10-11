import socket
import pygame
import threading
import sys
import random
import math
import time

HOST = ''
PORT = 50007
          
def consoles():
    global msg
    while True:
        x, col, hp, type, fire_rate = client.recv(1024).decode('utf-8').split(', ')
        print(x, col, hp, type)
        if type == "AppearZombie":
            zombies.append(Zombie(int(x), int(col), int(hp), type, float(fire_rate)))
        elif type == "AppearPlant":
            map[int(col)][int(x)] = Plant(int(x), int(col), type, int(hp), float(fire_rate))
        elif type == "DeletePlant":
            map[int(col)][int(x)] = 0
        # elif type == "shotremove":
        #     del shots[int(hp)]
        # elif type == "zombieremove":
        #     del zombies[int(hp)]


def acceptC():
    global client,server,addr
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    client,addr=server.accept()

    # client.sendall(senddata.encode('utf-8'))

    thr=threading.Thread(target=consoles,args=())
    #클라이언트로부터 받는 데이터를 관리하기위한
    #멀티쓰레딩(밑에는 데몬스레드라고 선언 -> c++로 따지면 detach와같습니다)
    thr.Daemon=True
    thr.start()


acceptC()

# 초기화
pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock() 

# 이미지 정의
cursor_image = pygame.image.load("ab.webp").convert_alpha()
cursor_image = pygame.transform.scale(cursor_image, ( 100, 80 ))
shovel_image = pygame.image.load("Shovel.png").convert_alpha()
shovel_image = pygame.transform.scale(shovel_image, ( 100, 100 ))
cursor_width, cursor_height = cursor_image.get_size()
# 색상 정의
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
aqua = (0, 255, 255)
# 사운드 정의
plant = pygame.mixer.Sound("SFX plant.mp3")
delete = pygame.mixer.Sound("SFX plant2.mp3")
SelectP = pygame.mixer.Sound("SFX seedlift.mp3")
shovel = pygame.mixer.Sound("SFX shovel.mp3")
shoot = pygame.mixer.Sound("SFX throw.mp3")
splat = pygame.mixer.Sound("SFX splat.mp3")
chomp = pygame.mixer.Sound("SFX chomp.mp3")
gulp = pygame.mixer.Sound("Voices gulp.mp3")

SelectedPlant = None
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

shots = []
zombies = []


class Plant:
    def __init__(self, row, col, type, hp, fire_rate = 3):
        plant.play()
        
        self.row = row # test
        self.col = col # test
        self.x = self.row * (box_size + margin)
        self.y = self.col * (box_size + margin)
        self.type = type
        self.hp = hp
        self.image = cursor_image # Demo
        self.rect = pygame.Rect(self.x + 10, self.y + 10, 80, 80)
        
        
        self.fire_rate = fire_rate  # 발사 간격 (초 단위)
        self.last_shot_time = time.time()  # 마지막 발사 시간

    def draw(self, SCREEN, box_size, margin):
        # print(self.row, self.col)
        SCREEN.blit(self.image, (self.x, self.y))
    def debug(self, SCREEN, box_size, margin):
        pygame.draw.rect(SCREEN, aqua, self.rect)

    def update(self, shots):
        # 현재 시간이 마지막 발사 시간에서 발사 간격을 더한 값보다 크면 발사
        if time.time() - self.last_shot_time >= self.fire_rate:
            shots.append(Shot(self.x+ 50, self.y + 10, "pea"))
            self.last_shot_time = time.time()  # 발사 시간 업데이트

            # print("싸발")
    def damage(self, damage):
        self.hp -= damage
        chomp.play()


class Shot:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.speed = 10
        self.damage = 50 # Demo
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
    def __init__(self, x, col, hp, type, fire_rate=1):
        self.x = x
        self.col = col
        self.y = self.col * (100 + margin)
        
        self.type = type
        self.speed = 0.5 
        self.hp = hp 
        self.power = 30 # danage
        self.rect = pygame.Rect(self.x, self.y, 50, 100)

        self.fire_rate = fire_rate  # 공격 간격 (초 단위)
        self.last_atk_time = time.time()  # 마지막 공격 시간

    def draw(self, SCREEN):
        pygame.draw.rect(SCREEN, ( 0, 0, 255 ), self.rect)
    def move(self):
        self.x -= self.speed
        self.rect = pygame.Rect(self.x, self.y, 50, 100)
    def damage(self, damage):
        self.hp -= damage
        splat.play()
    def attack(self, plant):
        if time.time() - self.last_atk_time >= self.fire_rate:
            plant.damage(self.power)
            self.last_atk_time = time.time()  # 공격 시간 업데이트
        self.x += self.speed
        self.rect = pygame.Rect(self.x, self.y, 50, 100)



# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # 사용자가 스페이스 키를 눌렀을 때
                if SelectedPlant == None:
                    SelectedPlant = "Pea"
                    SelectP.play()

                else:
                    SelectedPlant = None
                    shovel.play()
            if event.key == pygame.K_UP:
                if closest_box:
                    col = int(closest_box[1] / (box_size + margin))
                    zombies.append(Zombie(1100, col, 1000, "AppearZombie", 3))

                    data = f"1100, {col}, 1000, AppearZombie, 1"
                    client.sendall(data.encode('utf-8'))
                    # for i in range(5):
                    #     zombies.append(Zombie(1100, i, 100, "Normal"))

        if event.type == pygame.MOUSEBUTTONDOWN:
            if closest_box and min_distance <= max_distance:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                row =  int(closest_box[0] / (box_size + margin))
                col = int(closest_box[1] / (box_size + margin))
                print(row, col)
                if SelectedPlant and map[col][row] == 0:
                    map[col][row] = Plant(row, col, "AppearPlant", 500, 3)

                    data = f"{row}, {col}, 1000, AppearPlant, 3"
                    client.sendall(data.encode('utf-8'))
                    # plant.play()
                elif not(SelectedPlant) and not(map[col][row] == 0):
                    map[col][row] = 0

                    data = f"{row}, {col}, 1000, DeletePlant, 3"
                    client.sendall(data.encode('utf-8'))
                    delete.play()
            

                 
            
    # 화면 업데이트
    screen.fill((255, 255, 255))  # 화면을 흰색으로 채웁니다.



    mouse_x, mouse_y = pygame.mouse.get_pos()

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
                if SelectedPlant:
                    if map[col][row] == 0:
                        color = red  # 가장 가까운 상자 중에서 일정 거리 이내인 경우 빨간색으로 표시
                elif not(map[col][row] == 0):
                    color = blue
            else:
                color = black  # 나머지 상자는 검은색

            pygame.draw.rect(screen, color, (x, y, box_size, box_size))
            if (SelectedPlant) and closest_box == (x, y) and min_distance <= max_distance and map[col][row] == 0:
                cursor_image_copy = cursor_image.copy()  # 이미지를 복사
                cursor_image_copy.set_alpha(100)  # 복사본에 투명도 적용
                screen.blit(cursor_image_copy, (x, y))
            elif not(map[col][row] == 0):
                map[col][row].draw(screen, box_size, margin)
                # map[col][row].debug(screen, box_size, margin)
                map[col][row].update(shots)

                for zombie in zombies[:]:
                    if zombie.rect.colliderect(map[col][row].rect):
                        print("zombie atk")
                        zombie.attack(map[col][row])
                        
                        if map[col][row].hp <=0:
                            map[col][row] = 0

                            data = f"{row}, {col}, 1000, DeletePlant, 3"
                            client.sendall(data.encode('utf-8'))
                            gulp.play()
                            break

    
    # 움직임 + 화면 이탈
    for i, shot  in enumerate(shots[:]): # [:]은 리스트를 복제함
        if shot.x >= 1280:
            shots.remove(shot)

            data = f"{row}, {col}, {i}, shotremove, 3"
            client.sendall(data.encode('utf-8'))
        shot.move()
        shot.draw(screen)
        
        
    for i, zombie  in enumerate(zombies[:]):
        if zombie.x <= 0 or zombie.hp <= 0:
            zombies.remove(zombie)

            data = f"{row}, {col}, {i}, zombieremove, 3"
            client.sendall(data.encode('utf-8'))
        zombie.move()
        zombie.draw(screen)
        


    # 탄알이 좀비한테 맞았나
    for i, shot in enumerate(shots[:]):
        for f, zombie in enumerate(zombies[:]):
            if shot.rect.colliderect(zombie.rect):
                print("atk")
                shots.remove(shot)
                zombie.damage(shot.damage)

                data = f"{row}, {col}, {i}, shotremove, 3"
                client.sendall(data.encode('utf-8'))
                break

    # print(shots)
    # 커스텀 커서 이미지 그리기         
    x, y = pygame.mouse.get_pos()
    cursor_x = x - cursor_width // 2
    cursor_y = y - cursor_height // 2
    if (SelectedPlant):
        screen.blit(cursor_image, (cursor_x, cursor_y))
    else:
        screen.blit(shovel_image, (cursor_x, cursor_y))


    pygame.display.flip()  # 화면을 업데이트합니다.
    clock.tick(60)  # FPS를 60으로 설정합니다.

pygame.quit()
sys.exit()