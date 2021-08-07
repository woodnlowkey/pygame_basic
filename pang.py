import os
import pygame
# 기본 초기화----------------------------------------------------
pygame.init() # 초기화

screen_width = 640 # 가로크기
screen_height = 480 # 세로크기
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Pang") # 화면 타이틀

clock = pygame.time.Clock() #FPS

# 사용자 게임----------------------------------------------------

current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "images")

background = pygame.image.load(os.path.join(image_path, "background.png"))
# 배경이미지
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1] # 스테이지 높이

character = pygame.image.load(os.path.join(image_path, "character.png"))
# 케릭터 불러오기
character_size = character.get_rect().size # 크기 구하기
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = screen_width / 2 - character_width / 2 # 화면 가로 절반 위치 설정
character_y_pos = screen_height - stage_height - character_height # 화면 세로 가장 아래 위치 설정

to_x = 0 # 이동 할 좌표
to_y = 0
character_speed = 0.3 # 이동 속도

weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
# 무기 가져오기
weapon_size = weapon.get_rect().size # 크기 구하기
weapon_width = weapon_size[0]

weapons = []

weapon_speed = 7

ball_images = [
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
    pygame.image.load(os.path.join(image_path, "balloon2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3.png")),
    pygame.image.load(os.path.join(image_path, "balloon4.png"))]

ball_speed_y = [-18, -15, -12, -9]

balls = []

balls.append({
    "pos_x" : 10,
    "pos_y" : 10,
    "img_idx" : 0,
    "posto_x" : 3,
    "posto_y" : -6,
    "init_spd_y" : ball_speed_y[0]
})

weapon_to_remove = -1
ball_to_remove = -1

game_font = pygame.font.Font(None, 40) # 폰트 객체 생성(폰트, 크기)
total_time = 100
start_ticks = pygame.time.get_ticks() # 시작 시간

game_result = "Game Over"

running = True # 진행 중 루프
while running:
    dt = clock.tick(30) # 초당 프레임 수 설정

    for event in pygame.event.get(): # 이벤트 발생
        if event.type == pygame.QUIT: # 창 닫기
            running = False # 끔

        if event.type == pygame.KEYDOWN: # 방향키를 누르면
            if event.key == pygame.K_LEFT:
                to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                to_x += character_speed
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type == pygame.KEYUP: # 방향키를 떼면
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0

    character_x_pos += to_x * dt # 케릭터 이동

    if character_x_pos < 0: # 케릭터 이동 가로 경계값
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 무기 위치 조정
    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons]

    weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0]

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]
        # 가로 튕겨 나옴
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["posto_x"] = ball_val["posto_x"] * -1
        # 세로 튕겨 나옴
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["posto_y"] = ball_val["init_spd_y"]
        else:
            ball_val["posto_y"] += 0.5

        ball_val["pos_x"] += ball_val["posto_x"]
        ball_val["pos_y"] += ball_val["posto_y"]


    character_rect = character.get_rect() # 충돌처리
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y
    # 충돌 체크
        if character_rect.colliderect(ball_rect):
            running = False
            break

        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y
            
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx
                ball_to_remove = ball_idx

                if ball_img_idx < 3:

                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                        "img_idx" : ball_img_idx + 1,
                        "posto_x" : -3,
                        "posto_y" : -6,
                        "init_spd_y" : ball_speed_y[ball_img_idx + 1]})
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                        "img_idx" : ball_img_idx + 1,
                        "posto_x" : 3,
                        "posto_y" : -6,
                        "init_spd_y" : ball_speed_y[ball_img_idx + 1]})

                break
        else:
            continue
        break

    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    if len(balls) == 0:
        game_result = "Mission Complete"
        running = False

    screen.blit(background, (0, 0)) # 배경적용

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # 경과시간 초 단위로 표시
    timer = game_font.render(str("Time : {}".format(int(total_time - elapsed_time))), True, (255, 255, 255))
    screen.blit(timer, (10, 10))

    if total_time - elapsed_time <= 0:
        game_result = "Time Over"
        running = False

    pygame.display.update() # 게임화면 다시 적용

msg = game_font.render(game_result, True, (255, 255, 0))
msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)
pygame.display.update()

pygame.time.delay(2000)

pygame.quit()