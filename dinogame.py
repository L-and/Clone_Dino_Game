import os
import pygame
from time import sleep
from random import randint
###############################################################################################
# 기본 초기화 (반드시 해야 하는 것들)

pygame.init()

# 화면 크기 설정
screen_width = 1200  # 가로 크기
screen_height = 700  # 세로 크기

screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Clone dino game")  # 게임 이름

# FPS
clock = pygame.time.Clock()
###############################################################################################

# 1. 사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 속도, 폰트 등)
current_path = os.path.dirname(__file__)  # 현재 파일의 위치를 반환
image_path = os.path.join(current_path, "images")  # images 폴더 위치 반환
sound_path = os.path.join(current_path, "sounds")  # sounds 폴더 위치 반환

# 배경 만들기
background = pygame.image.load(os.path.join(image_path, "background.png"))
screen_x_pos = 0  # 배경을 움직이기위해 사용

# 스테이지 만들기
stage = pygame.image.load(os.path.join(image_path,  "stage.png"))
stage_rect = stage.get_rect().size
stage_height = stage_rect[1]  # 스테이지의 높이 위에 캐릭터를 두기 위해 사용
stage_x_pos = 0  # 스테이지를 움직이기위해 사용

# 게임오버,게임승리 화면
game_over = pygame.image.load(os.path.join(image_path, "game_over.png"))
game_win = pygame.image.load(os.path.join(image_path, "game_win.png"))

# 캐릭터 만들기
character_gif = [pygame.image.load(os.path.join(image_path, "c1.png")),
                 pygame.image.load(os.path.join(image_path, "c2.png")),
                 pygame.image.load(os.path.join(image_path, "c3.png")),
                 pygame.image.load(os.path.join(image_path, "c4.png"))]
gif_count = 0
gif_speed = 10

character = pygame.image.load(os.path.join(image_path, "c1.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = 100
character_y_pos = screen_height - stage_height - character_height

######점프######

# 캐릭터 점프 속도
character_to_y = 0
isJump = False
Jump_Height = 20
jumpCount = Jump_Height # 점프 높이


jump_sound = pygame.mixer.Sound(os.path.join(sound_path, "jump_sound.wav"))
jump_sound.set_volume(0.3)


################
# 적 만들기
enemy_images = [
    pygame.image.load(os.path.join(image_path, "enemy1.png")),
    pygame.image.load(os.path.join(image_path, "enemy2.png"))
]

enemy_size = [
    enemy_images[0].get_rect().size,
    enemy_images[1].get_rect().size
]

enemy_width = [
    enemy_size[0][0],
    enemy_size[1], [0]
]

enemy_height = [
    enemy_size[0][1],
    enemy_size[1][1]
]

enemy_x_pos = [1200, 1200]
enemy_y_pos = [
    screen_height - stage_height - enemy_height[0],
    screen_height - stage_height - enemy_height[1]
]

# 적들
enemys = []

# 적 스폰 여부
is_spawn = False
spawn_cool = True

move_speed = 1  # 스테이지,적 이동속도

# 적 스폰 시간 저장
enemy_spawn_tmp = 0

# 적 스폰시간 간격
enemy_spawn_time = 1

# 점수
score = 0
win_score = 30

# 게임 시간 정의
start_ticks = pygame.time.get_ticks()  # 시작 시간 정의

# 폰트 정의
game_font = pygame.font.Font(None, 40)


running = True
is_game_over = False
is_game_win = False
while running:
    dt = clock.tick(60)

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if not(isJump):
                if event.key == pygame.K_SPACE:
                    jump_sound.play()
                    isJump = True

    # 경과 시간 계산
    elapsed_time = int((pygame.time.get_ticks() - start_ticks) / 1000)

    # 게임 캐릭터 위치 정의
    character_y_pos += character_to_y * dt

    # 캐릭터 점프
    if isJump == True:
        if jumpCount >= -Jump_Height:
            character_y_pos -= (jumpCount * abs(jumpCount)) * 0.1
            jumpCount -= 1
        else:
            jumpCount = Jump_Height
            isJump = False

    # 배경 이동
    screen_x_pos += move_speed * dt

    if screen_x_pos >= 1200:
        screen_x_pos = 0

    # 스테이지 이동
    stage_x_pos += move_speed * dt

    if stage_x_pos >= 1200:
        stage_x_pos = 0
    # 캐릭터 gif
    if(gif_count < (4 * gif_speed - 1)):
        gif_count += 1
    else:
        gif_count = 0

    # 적 랜덤생성
    if (elapsed_time % enemy_spawn_time) * dt == 0 and spawn_cool == True:
        enemy_spawn_tmp = elapsed_time
        is_spawn = True
        spawn_cool = False

    if is_spawn == True:
        enemy_type = randint(0, 1)
        if enemy_type == 0:
            enemys.append({
                "pos_x": enemy_x_pos[0],
                "pos_y": enemy_y_pos[0],
                "img_idx": 0
            })
        elif enemy_type == 1:
            enemys.append({
                "pos_x": enemy_x_pos[1],
                "pos_y": enemy_y_pos[1],
                "img_idx": 1
            })
        is_spawn = False

    if enemy_spawn_tmp + 1 == elapsed_time:
        spawn_cool = True

    # 적 이동
    for idx, val in enumerate(enemys):
        val["pos_x"] -= move_speed * dt

    # 화면 밖으로 벗어난 적 제거 + 점수 증가
    for idx, val in enumerate(enemys):
        if val["pos_x"] < 0 - enemy_width[0]:
            del enemys[idx]
            score += 1

    # 게임승리
    if(score >= win_score):
        is_game_win = True
        running = False

    # 4. 충돌 처리

    # 캐릭터 rect 정보 업데이트
    character_rect = character_gif[int(gif_count / gif_speed)].get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    # 적 rect 정보 업데이트
    for enemy_idx, enemy_val in enumerate(enemys):
        enemy_pos_x = enemy_val["pos_x"]
        enemy_pos_y = enemy_val["pos_y"]
        enemy_img_idx = enemy_val["img_idx"]

        enemy_rect = enemy_images[enemy_img_idx].get_rect()
        enemy_rect.left = int(enemy_pos_x)
        enemy_rect.top = int(enemy_pos_y)

        if character_rect.colliderect(enemy_rect):  # 적과 충돌하면
            running = False
            is_game_over = True

    # 5. 화면에 그리기
    screen.blit(background, (-screen_x_pos, 0))
    screen.blit(background, (1200 - screen_x_pos, 0))

    screen.blit(stage, (-stage_x_pos, screen_height - stage_height))
    screen.blit(stage, (1200 - stage_x_pos, screen_height - stage_height))

    screen.blit(character_gif[int(gif_count / gif_speed)],
                (int(character_x_pos), int(character_y_pos)))

    for idx, val in enumerate(enemys):
        enemy_pos_x = val["pos_x"]
        enemy_pos_y = val["pos_y"]
        enemy_img_idx = val["img_idx"]
        screen.blit(enemy_images[enemy_img_idx],
                    (int(enemy_pos_x), int(enemy_pos_y)))

    score_font = game_font.render(str(score), True, (88, 255, 88))

    screen.blit(score_font, (10, 10))

    pygame.display.update()

    #######게임종료화면 출력######
    if(is_game_win == True):
        screen.blit(game_win, (0, 0))
        pygame.display.update()
        sleep(2.5)

    if(is_game_over == True):
        screen.blit(game_over, (0, 0))
        pygame.display.update()
        sleep(2.5)

    ############################
pygame.quit()
