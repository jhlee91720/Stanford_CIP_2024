import os
import pygame

# 게임 초기화 #################################################################################
pygame.init()

screen_width = 640 # 가로 크기
screen_height = 480 # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("PANG!")

clock = pygame.time.Clock()
###########################################################################################



# 사용자 게임 초기화 ##########################################################################
current_path = os.path.dirname(__file__)  # 현재 파일의 위치를 반환
image_path = os.path.join(current_path, "assets")  # assets 폴더 위치를 반환

# 1. 배경 만들기
background = pygame.image.load(os.path.join(image_path, "Background.png")) # 배경 이미지 불러오기

# 2. 스테이지 만들기
stage = pygame.image.load(os.path.join(image_path, "Stage.png")) # 스테이지 이미지 불러오기
stage_size = stage.get_rect().size # 스테이지 이미지 크기
stage_height = stage_size[1] # 스테이지 높이

# 3. 캐릭터 만들기
character = pygame.image.load(os.path.join(image_path, "Character.png")) # 캐릭터 이미지 불러오기
character_size = character.get_rect().size # 캐릭터 이미지 크기
character_width = character_size[0] # 캐릭터 너비
character_height = character_size[1] # 캐릭터 높이
character_x_pos = (screen_width / 2) - (character_width / 2) # 캐릭터 x 좌표
character_y_pos = screen_height - character_height - stage_height # 캐릭터 y 좌표
character_to_x = 0 # 캐릭터 이동 좌표
character_speed = 5 # 캐릭터 이동 속도

# 4. 무기 만들기
weapon = pygame.image.load(os.path.join(image_path, "Weapon.png")) # 무기 이미지 불러오기
weapon_size = weapon.get_rect().size # 무기 이미지 크기
weapon_width = weapon_size[0] # 무기 너비
weapons = [] # 무기 여러번 발사 가능
weapon_speed = 10 # 무기 속도

# 5. 공 만들기
ball_images = [
    pygame.image.load(os.path.join(image_path, "Balloon_1.png")),
    pygame.image.load(os.path.join(image_path, "Balloon_2.png")),
    pygame.image.load(os.path.join(image_path, "Balloon_3.png")),
    pygame.image.load(os.path.join(image_path, "Balloon_4.png"))
]
ball_speed_y = [-18, -15, -12, -9] # 공 크기별 y축 이동 속도
balls = [] # 공 여러개 생성 가능
balls.append({ # 첫 번째 공 추가
    "pos_x": 50, # 공 x 좌표
    "pos_y": 50, # 공 y 좌표
    "img_idx": 0, # 공 이미지 인덱스
    "to_x": 3, # 공 x 이동 방향
    "to_y": -6, # 공 y 이동 방향
    "init_spd_y": ball_speed_y[0] # 공 초기 속도
})

# 6. 사라진 공 & 무기 
weapon_to_remove = -1
ball_to_remove = -1

# 7. 폰트 정의
game_font = pygame.font.Font(None, 40)
total_time = 100
start_ticks = pygame.time.get_ticks() # 시작 시간 정의

# 8. 게임 종료 메세지
game_result = "Game Over"

running = True # 게임이 진행중인가?
while running: #while = 계속 돌리는 명령어
    dt = clock.tick(30) # 게임화면의 초당 프레임 수를 설정
##########################################################################################


# 이벤트 처리 #####################################################################################
    for event in pygame.event.get():  # 어떤 이벤트가 발생하였는가? 키보드, 마우스등 이벤트가 발생하면 반응
        if event.type == pygame.QUIT: # 창이 닫히는 이벤트가 발생하였는가? 발생하면 게임이 닫힘
            running = False # 게임이 진행중이 아님

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: # 캐릭터를 왼쪽으로
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT: # 캐릭터를 오른쪽으로
                character_to_x += character_speed  
            elif event.key == pygame.K_SPACE: # 무기 발사
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0     

# 3. 게임 캐릭터 위치 정의
    character_x_pos += character_to_x 

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width   
     
# 무기 위치 조정
# 100, 200 -> 180, 160, 140, ...
# 500, 200 -> 180, 160, 140, ...  
    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons] # 무기 위치를 위로

    # 천장에 닿은 무기 없애기
    weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0]

    # 공 위치 정의
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # 가로벽에 닿았을 때 공 이동 위치 변경 (튕겨 나오는 효과)
        if ball_pos_x <= 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1

        # 세로 위치
        # 스테이지에 튕겨서 올라가는 처리
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]    
        else: # 그 외의 모든 경우에는 속도를 증가     
            ball_val["to_y"] += 0.5

        ball_val["pos_x"] += ball_val["to_x"]   
        ball_val["pos_y"] += ball_val["to_y"]     

    # 4. 충돌 처리


    # 캐릭터 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        # 공 rect 정보 업데이트
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        # 공과 캐릭터 충돌 처리
        if character_rect.colliderect(ball_rect):
            running = False
            break
        
        # 공과 무기들 충돌 처리를
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            # 무기 rect 정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            # 충돌 체크 
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx # 해당 무기 없애기 위한 값 설정
                ball_to_remove = ball_idx # 해당 공 없애기 위한 값 설정

                # 가증 작은 크기의 공이 아니라면 다음 단계의 공으로 나눠주기
                if ball_img_idx < 3:
                    # 현재 공 크기 정보를 가지고 옴
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    # 나눠진 공 정보
                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    # 왼쪽으로 튕겨나가는 작은 공     
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width /2), # 공의 x 좌표
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2), # 공의 y 좌표
                        "img_idx" : ball_img_idx + 1, # 공의 이미지 인덱스
                        "to_x": -3, # 공의 x축 이동방향, -3 이면 왼쪽으로, 3이면 오른쪽으로
                        "to_y": -6, # 공의 y축 이동방향,
                        "init_spd_y": ball_speed_y[ball_img_idx + 1]}) # y 최초 속도

                    # 오른쪽으로 튕겨나가는 작은 공     
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width /2), # 공의 x 좌표
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2), # 공의 y 좌표
                        "img_idx" : ball_img_idx + 1, # 공의 이미지 인덱스
                        "to_x": 3, # 공의 x축 이동방향, -3 이면 왼쪽으로, 3이면 오른쪽으로
                        "to_y": -6, # 공의 y축 이동방향,
                        "init_spd_y": ball_speed_y[ball_img_idx + 1]}) # y 최초 속도

                break
        else: # 계속 게임을 진행
            continue # 안쪽 for 문 조건이 맞지 않으면 continue. 바깥 for 문 계속 수행
        break # 안쪽 for 문에서 break 를 만나면 여기로 진입 가능. 2중 for 문을 한번에 탈출

# 충돌된 공 or 무기 없애기            
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1      

# 모든 공을 없앤 경우 게임 종료 (성공)
    if len(balls) == 0:
        game_result = "Mission Complete"
        running = False

# 5. 화면에 그리기
    screen.blit(background, (0, 0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]

        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))

# 경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 #  ms -> s
    timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)), True, (255, 255, 255))
    screen.blit(timer, (10, 10))

# 시간 초과했다면
    if total_time - elapsed_time <= 0:
        game_result = "Time Over"
        running = False

    pygame.display.update() # 게임화면을 다시 그리기(배경을 계속 갱신해주는 느낌)

# 게임 종료 메세지 #######################################################
msg = game_font.render(game_result, True, (255, 255, 0)) # 노란색
msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)
pygame.display.update()

pygame.time.delay(2000) # 2초 대기

pygame.quit()

