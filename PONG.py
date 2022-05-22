import pygame
import secrets
import os
import time


class Pong:

    # The coordinates of the paddles
    __p1_coords = (20, 0)
    __p2_coords = (920, 0)

    # Size and colour of the paddles
    __PADDLE_WIDTH = 20
    __PADDLE_HEIGHT = 100
    __PADDLE_COLOUR = (255, 255, 255)

    # Size and colour of the ball
    __ball_center = (470, 260)
    __BALL_COLOUR = __PADDLE_COLOUR
    __BALL_SIZE = 20

    # Movement speed for the paddles and the ball
    __paddle_vsp = 7
    __ball_speed = 5

    # Settings for the window: 960x540 with black background
    __WINDOW_WIDTH = 960
    __WINDOW_HEIGHT = 540
    __WINDOW_BG = (0, 0, 0)

    # Run the game at 60 FPS
    __CLOCK_TICKS = 60

    # Flag used to inform the main loop to end the game
    __end = False

    # Score of the players
    __score_p1 = 0
    __score_p2 = 0
    __win_score = 15

    def __init__(self):
        # Pygame initialization
        # Init window to 960x540
        pygame.init()
        window_size = (self.__WINDOW_WIDTH, self.__WINDOW_HEIGHT)
        self.__game_window = pygame.display.set_mode(window_size)
        pygame.display.set_caption('Python PONG')

        self.__game_clock = pygame.time.Clock()
        self.__paddle1 = pygame.Rect(self.__p1_coords,
                                     (self.__PADDLE_WIDTH, self.__PADDLE_HEIGHT))
        self.__paddle2 = pygame.Rect(self.__p2_coords,
                                     (self.__PADDLE_WIDTH, self.__PADDLE_HEIGHT))
        self.__ball = pygame.Rect(self.__ball_center,
                                  (self.__BALL_SIZE, self.__BALL_SIZE))

        # Select a random direction
        # The secrets module is used instead of the random one
        # to give a more random feel to the choice.
        possible_dirs = [-1, 1]
        self.__ball_direction_y = secrets.choice(possible_dirs)
        self.__ball_direction_x = secrets.choice(possible_dirs)

        # Load sound effects
        self.__sfx_paddle = pygame.mixer.Sound(os.path.join('sfx', 'paddle.mp3'))
        self.__sfx_wall = pygame.mixer.Sound(os.path.join('sfx', 'wall.mp3'))
        self.__sfx_score = pygame.mixer.Sound(os.path.join('sfx', 'score.mp3'))

        self.__begin = False

    def end(self):
        return self.__end

    def update(self):

        # Start the game if the user presses the space bar
        # End the game if the user presses Escape or someone wins
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__end = True
                    return
                if event.key == pygame.K_SPACE:
                    self.__begin = True
                    return

        if not self.__begin:
            pygame.display.set_caption('Python PONG - Press SPACE to start!')
            return


        # Update the score on the title bar
        window_title = 'Python PONG - %d:%d - %d FPS' % (self.__score_p1,
                                                         self.__score_p2,
                                                         int(self.__game_clock.get_fps()))
        pygame.display.set_caption(window_title)

        # Set background colour
        self.__game_window.fill(self.__WINDOW_BG)

        # Draw the paddles and the ball in the position
        # computed at the end of the previous frame
        self.__draw_paddle(self.__game_window, self.__paddle1)
        self.__draw_paddle(self.__game_window, self.__paddle2)
        self.__draw_ball(self.__game_window, self.__ball)

        # Move paddles
        self.__move_paddles()

        # Move the ball
        self.__move_ball()

        # Check for collision with paddles
        if self.__ball_collide_paddle():
            self.__sfx_paddle.play()  # Play a bounce sound effect
            self.__ball_direction_x *= -1  # Invert motion on the horizontal axis, simulating bounce

            possible_dirs = [-1, 1]  # Select a random direction on the vertical axis
            self.__ball_direction_y *= secrets.choice(possible_dirs)

        # Move the ball according to the computed direction
        self.__ball.y = self.__ball.y + self.__ball_direction_y * self.__ball_speed
        self.__ball.x = self.__ball.x + self.__ball_direction_x * self.__ball_speed

        if self.__score_p1 >= self.__win_score:
            pygame.display.set_caption('Python PONG - Player 1 wins!')
            time.sleep(1)
            self.__end = True
            return
        elif self.__score_p2 >= self.__win_score:
            pygame.display.set_caption('Python PONG - Player 2 wins!')
            time.sleep(1)
            self.__end = True
            return

        pygame.display.update()  # Render everything
        self.__game_clock.tick(self.__CLOCK_TICKS)

    def __move_paddles(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            if self.__paddle1.y < self.__WINDOW_HEIGHT - self.__PADDLE_HEIGHT:
                self.__paddle1.y += self.__paddle_vsp
        elif keys[pygame.K_w]:
            if self.__paddle1.y > 0:
                self.__paddle1.y -= self.__paddle_vsp
        elif keys[pygame.K_DOWN]:
            if self.__paddle2.y < self.__WINDOW_HEIGHT - self.__PADDLE_HEIGHT:
                self.__paddle2.y += self.__paddle_vsp
        elif keys[pygame.K_UP]:
            if self.__paddle2.y > 0:
                self.__paddle2.y -= self.__paddle_vsp

    def __move_ball(self):
        # When the ball touches the top or bottom of
        # the playfield it inverts its vertical direction
        if self.__ball.y <= 0:
            self.__sfx_wall.play()
            self.__ball_direction_y = 1
        elif self.__ball.y > self.__WINDOW_HEIGHT - self.__BALL_SIZE:
            self.__sfx_wall.play()
            self.__ball_direction_y = -1

        # When the ball touches the left or right side
        # of the playfield (aka beyond the paddles), the ball resets to the center,
        # a sound effect plays,
        # a point is assigned to the corresponding player
        # and the game waits 1 sec to give some time to the players
        if self.__ball.x <= self.__paddle1.x:  # was 0
            self.__ball.x = self.__ball_center[0]
            self.__ball.y = self.__ball_center[1]
            self.__sfx_score.play()
            self.__score_p2 += 1
            time.sleep(1)
        elif self.__ball.x > self.__paddle2.x:  # was self.__WINDOW_WIDTH - self.__BALL_SIZE
            self.__ball.x = self.__ball_center[0]
            self.__ball.y = self.__ball_center[1]
            self.__sfx_score.play()
            self.__score_p1 += 1
            time.sleep(1)

    def __draw_paddle(self,  game_win, paddle):
        pygame.draw.rect(game_win, self.__PADDLE_COLOUR, paddle)

    def __draw_ball(self, game_win, ball):
        pygame.draw.rect(game_win, self.__PADDLE_COLOUR, ball)

    def __ball_collide_paddle(self):
        if self.__ball.x <= self.__paddle1.x + self.__PADDLE_WIDTH and self.__paddle1.y <= self.__ball.y <= self.__paddle1.y + self.__PADDLE_HEIGHT:
            return True
        elif self.__ball.x + self.__BALL_SIZE >= self.__paddle2.x and self.__paddle2.y <= self.__ball.y <= self.__paddle2.y + self.__PADDLE_HEIGHT:
            return True
        else:
            return False
