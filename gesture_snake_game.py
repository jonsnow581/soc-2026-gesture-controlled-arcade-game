import cv2 as cv
import mediapipe as mp
import math
import time
import pygame
import random
import sys

#short variable names for mp classes
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

#configuring the detector
options = HandLandmarkerOptions(base_options = BaseOptions(model_asset_path = "hand_landmarker.task"), running_mode = VisionRunningMode.VIDEO, num_hands = 1)

#defining grid dimensions
CELL_SIZE   = 30
GRID_WIDTH  = 30
GRID_HEIGHT = 22
WIDTH = CELL_SIZE * GRID_WIDTH
HEIGHT = CELL_SIZE * GRID_HEIGHT

#colors
BG_COLOR = (15, 15, 25)
SNAKE_HEAD = (0, 230, 120)
SNAKE_BODY = (0, 170, 90)
FOOD_COLOR = (240, 70, 90)
TEXT_COLOR = (235, 235, 245)
GRID_COLOR = (30, 30, 45)

#helper game functions
def random_food(snake):
    while True:
        pos = (random.randint(2, GRID_WIDTH - 3), random.randint(2, GRID_HEIGHT - 3))
        if pos not in snake:
            return pos

def draw_cell(surface, pos, color):
    x = pos[0] * CELL_SIZE
    y = pos[1] * CELL_SIZE
    rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, BG_COLOR, rect, 1)

def quit_game(cap):
    cap.release()
    cv.destroyAllWindows()
    pygame.quit()
    sys.exit()

#MAIN LOOP
def main():

    #initializing pygame and setting up the window
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Gesture Controlled Snake")
    font = pygame.font.SysFont("consolas", 22)
    big_font = pygame.font.SysFont("consolas", 40, bold=True)
    
    
    #setting up webcam feed
    cap =cv.VideoCapture(0)

    #initializing game variables
    def reset_game():
        start = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        return [start], (1, 0), random_food([start]), 0

    snake, direction, food, score = reset_game()
    game_over = False
    is_paused = False
    game_started = False    
    high_score = 0          

    #game speed variables
    MOVE_DELAY_START = 500               # starting speed (ms between steps)
    MOVE_DELAY_MIN = 80                  # fastest the snake can ever get
    SPEED_STEP = 5                       # how many ms to shave off per food eaten
    MOVE_DELAY = MOVE_DELAY_START        # current delay, will shrink as score grows
    last_move_time = pygame.time.get_ticks()

    #setting up stability filters
    stable_gesture = "NONE"
    prev_gesture = "NONE"
    gesture_counter = 0
    STABLE_FRAMES = 3

    with HandLandmarker.create_from_options(options) as landmarker:
        while True:

            success, frame = cap.read()

            #breaking the loop if the webcam is not detected
            if not success:
                print("CAM NOT DETECTED")
                break

            #flipping the frame bcs its mirrored
            frame = cv.flip(frame, 1)

            #coverting BGR to RGB for mediapipe
            rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

            #wrapping the numpy array into a mediapipe Image obj
            mp_image = mp.Image(image_format = mp.ImageFormat.SRGB, data = rgb_frame)

            #detecting hand landmarks
            frame_timestamp_ms = int(time.time() * 1000)
            result = landmarker.detect_for_video(mp_image, frame_timestamp_ms)
            angle = 0.0

            if result.hand_landmarks: #will not run if the list result.hand_landmarks is empty

                handLms = result.hand_landmarks[0]

                handedness_label = result.handedness[0][0].display_name
                handedness_label = "Left" if handedness_label == "Right" else "Right"

                HAND_CONNECTIONS = [
                    (0,1),(1,2),(2,3),(3,4),        # thumb
                    (0,5),(5,6),(6,7),(7,8),        # index
                    (5,9),(9,10),(10,11),(11,12),   # middle
                    (9,13),(13,14),(14,15),(15,16), # ring
                    (13,17),(17,18),(18,19),(19,20),# pinky
                    (0,17)                          # wrist to pinky base
                ]

                def draw_landmarks(frame, hand_landmarks):
                    h, w, _ = frame.shape
                    points = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks]

                    for start, end in HAND_CONNECTIONS:
                        cv.line(frame, points[start], points[end], (0, 255, 0), 2)

                    for point in points:
                        cv.circle(frame, point, 5, (0, 0, 255), -1)

                draw_landmarks(frame, handLms)

                #creating a list of fingers which are stretched
                fingers_up = []

                thumb_tip, thumb_ip = handLms[4], handLms[3]
                index_tip, index_mcp = handLms[8], handLms[5]

                #checking if the thumb is up
                if handedness_label == "Right":
                    fingers_up.append(thumb_tip.x < thumb_ip.x)
                else:
                    fingers_up.append(thumb_tip.x > thumb_ip.x)

                #checking the same for the others
                for tip in [8,12,16,20]:
                    fingers_up.append(handLms[tip].y < handLms[tip - 2].y)

                count = sum(fingers_up)

                #angle calc
                dx = index_tip.x - index_mcp.x
                dy = index_tip.y - index_mcp.y
                angle = math.degrees(math.atan2(-dy, dx))

                #identifying hand gestures using the landmarks
                if count == 0:
                    gesture = "FIST"

                elif count == 5:
                    gesture = "PALM"

                else:
                    if -45<= angle <=45:
                        gesture = "RIGHT"
                    elif 45< angle <=135:
                        gesture = "UP"
                    elif 135< angle <=180 or -180<= angle <=-135:
                        gesture = "LEFT"
                    elif -135< angle <-45:
                        gesture = "DOWN"

                


                #stability filter
                if gesture == prev_gesture:
                    gesture_counter += 1
                
                else:
                    gesture_counter = 0
                    prev_gesture = gesture

                if gesture_counter >= STABLE_FRAMES:
                    stable_gesture = gesture

            #event handling and updating game state
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cap.release()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.QUIT:
                    quit_game(cap)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    quit_game(cap)

            # Direction tracking changes instantly when you point
            if not game_started:
                if stable_gesture == "FIST":
                    game_started = True
                    snake, direction, food, score = reset_game()
                    stable_gesture = "NONE"
                    last_move_time = pygame.time.get_ticks() # Reset clock
                    MOVE_DELAY = MOVE_DELAY_START   # reset speed on restart
            elif game_over:
                if stable_gesture == "FIST":
                    snake, direction, food, score = reset_game()
                    game_over = False
                    stable_gesture = "NONE"
                    last_move_time = pygame.time.get_ticks() # Reset clock
                    MOVE_DELAY = MOVE_DELAY_START   # reset speed on restart
            else:
                if stable_gesture == "PALM":
                    is_paused = True
                elif stable_gesture in ["UP", "DOWN", "LEFT", "RIGHT"]:
                    is_paused = False

                if not is_paused:
                    if stable_gesture == "UP" and direction != (0, 1):
                        direction = (0, -1)
                    elif stable_gesture == "DOWN" and direction != (0, -1):
                        direction = (0, 1)
                    elif stable_gesture == "LEFT" and direction != (1, 0):
                        direction = (-1, 0)
                    elif stable_gesture == "RIGHT" and direction != (-1, 0):
                        direction = (1, 0)

            current_time = pygame.time.get_ticks()
            
            
            if game_started and not game_over and not is_paused and (current_time - last_move_time > MOVE_DELAY):
                last_move_time = current_time # Reset time anchor for next step
                
                head = snake[0]
                new_head = (head[0] + direction[0], head[1] + direction[1])

                hit_wall = (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT)
                hit_self = new_head in snake

                if hit_wall or hit_self:
                    game_over = True
                    if score > high_score:      # update high score when the game ends
                        high_score = score
                else:
                    snake.insert(0, new_head)
                    if new_head == food:
                        score += 1
                        food = random_food(snake)
                        MOVE_DELAY = max(MOVE_DELAY_MIN, MOVE_DELAY - SPEED_STEP)      #speed up, but never below minimum
                    else:
                        snake.pop()

            screen.fill(BG_COLOR)

            if not game_started:
                #WELCOME SCREEN
                title_surf = big_font.render("GESTURE SNAKE", True, SNAKE_HEAD)
                sub_surf = font.render("Make a FIST to start", True, TEXT_COLOR)
                screen.blit(title_surf, (WIDTH//2 - title_surf.get_width()//2, HEIGHT//2 - 40))
                screen.blit(sub_surf, (WIDTH//2 - sub_surf.get_width()//2, HEIGHT//2 + 20))

            else:
                for gx in range(GRID_WIDTH):
                    pygame.draw.line(screen, GRID_COLOR, (gx*CELL_SIZE, 0), (gx*CELL_SIZE, HEIGHT))
                for gy in range(GRID_HEIGHT):
                    pygame.draw.line(screen, GRID_COLOR, (0, gy*CELL_SIZE), (WIDTH, gy*CELL_SIZE))

                draw_cell(screen, food, FOOD_COLOR)
                for i, segment in enumerate(snake):
                    color = SNAKE_HEAD if i == 0 else SNAKE_BODY
                    draw_cell(screen, segment, color)

                score_surf = font.render(f"Score: {score} | Gesture: {stable_gesture}", True, TEXT_COLOR)
                hs_surf = font.render(f"Best: {high_score}", True, (255, 215, 0))    # gold color
                screen.blit(score_surf, (8, 6))
                screen.blit(hs_surf, (WIDTH - hs_surf.get_width() - 8, 6))    # pin to top right corner


                if is_paused and not game_over:
                    pause_surf = big_font.render("PAUSED", True, TEXT_COLOR)
                    sub_surf = font.render("Point in any direction to resume", True, TEXT_COLOR)
                    screen.blit(pause_surf, (WIDTH//2 - pause_surf.get_width()//2, HEIGHT//2 - 40))
                    screen.blit(sub_surf, (WIDTH//2 - sub_surf.get_width()//2, HEIGHT//2 + 15))

                if game_over:
                    msg = big_font.render("GAME OVER", True, FOOD_COLOR)
                    sub = font.render("Make a FIST to restart", True, TEXT_COLOR)
                    screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 40))
                    screen.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//2 + 15))

            pygame.display.flip()

            cv.putText(frame, f"Gesture: {stable_gesture}", (10, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv.imshow("Vision Tracking Feedback", frame)
            
            if cv.waitKey(1) & 0xFF == ord('q'):
                quit_game(cap)
                break

    cap.release()
    cv.destroyAllWindows()
    pygame.quit()

if __name__ == "__main__":
    main()

                

                

                
                

        