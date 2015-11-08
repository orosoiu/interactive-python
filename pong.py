# Implementation of classic arcade game Pong

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
BALL_SPEED_X_INITIAL = 2
BALL_SPEED_Y_INITIAL = 1
BALL_SPEED_INCREMENT = 1
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
PADDLE_VEL = 3


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel  # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    if direction == "RIGHT":
        ball_vel = [BALL_SPEED_X_INITIAL, -BALL_SPEED_Y_INITIAL]
    else:
        ball_vel = [-BALL_SPEED_X_INITIAL, -BALL_SPEED_Y_INITIAL]


def recalculate_ball_position():
    global ball_pos, ball_vel
    # reflect from upper wall
    if ball_pos[1] < BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    # reflect from lower wall
    if ball_pos[1] > HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]

    ball_pos[0] = ball_pos[0] + ball_vel[0]
    ball_pos[1] = ball_pos[1] + ball_vel[1]


def draw_left_paddle(canvas):
    global paddle1_pos
    left_paddle_upper_left = [x + y for x, y in zip(paddle1_pos, [-HALF_PAD_WIDTH, -HALF_PAD_HEIGHT])]
    left_paddle_upper_right = [x + y for x, y in zip(paddle1_pos, [HALF_PAD_WIDTH, -HALF_PAD_HEIGHT])]
    left_paddle_lower_left = [x + y for x, y in zip(paddle1_pos, [-HALF_PAD_WIDTH, HALF_PAD_HEIGHT])]
    left_paddle_lower_right = [x + y for x, y in zip(paddle1_pos, [HALF_PAD_WIDTH, HALF_PAD_HEIGHT])]
    canvas.draw_polygon(
        [left_paddle_upper_left, left_paddle_upper_right, left_paddle_lower_right, left_paddle_lower_left],
        2, "White", "White")


def draw_right_paddle(canvas):
    global paddle2_pos
    right_paddle_upper_left = [x + y for x, y in zip(paddle2_pos, [-HALF_PAD_WIDTH, -HALF_PAD_HEIGHT])]
    right_paddle_upper_right = [x + y for x, y in zip(paddle2_pos, [HALF_PAD_WIDTH, -HALF_PAD_HEIGHT])]
    right_paddle_lower_left = [x + y for x, y in zip(paddle2_pos, [-HALF_PAD_WIDTH, HALF_PAD_HEIGHT])]
    right_paddle_lower_right = [x + y for x, y in zip(paddle2_pos, [HALF_PAD_WIDTH, HALF_PAD_HEIGHT])]
    canvas.draw_polygon(
        [right_paddle_upper_left, right_paddle_upper_right, right_paddle_lower_right, right_paddle_lower_left],
        2, "White", "White")


def recalculate_left_paddle_position():
    global paddle1_pos, paddle1_vel
    # paddles can only move on y axis
    paddle1_pos[1] += paddle1_vel[1]
    # keep in boundaries
    if paddle1_pos[1] > HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos[1] = HEIGHT - HALF_PAD_HEIGHT
    if paddle1_pos[1] < HALF_PAD_HEIGHT:
        paddle1_pos[1] = HALF_PAD_HEIGHT


def recalculate_right_paddle_position():
    global paddle2_pos, paddle2_vel
    # paddles can only move on y axis
    paddle2_pos[1] += paddle2_vel[1]
    # keep in boundaries
    if paddle2_pos[1] > HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos[1] = HEIGHT - HALF_PAD_HEIGHT
    if paddle2_pos[1] < HALF_PAD_HEIGHT:
        paddle2_pos[1] = HALF_PAD_HEIGHT


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints

    paddle1_pos = [HALF_PAD_WIDTH, HEIGHT / 2]
    paddle2_pos = [WIDTH - HALF_PAD_WIDTH, HEIGHT / 2]
    paddle1_vel = [0, 0]
    paddle2_vel = [0, 0]
    score1, score2 = 0, 0

    spawn_ball("RIGHT")


def check_win_conditions():
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel

    # if ball in left gutter and outside left paddle position
    if ball_pos[0] < PAD_WIDTH + BALL_RADIUS:
        if ball_pos[1] < (paddle1_pos[1] - HALF_PAD_HEIGHT) \
                or ball_pos[1] > (paddle1_pos[1] + HALF_PAD_HEIGHT):
            # player 2 wins
            score2 += 1
            spawn_ball("RIGHT")
        else:
            bounce_ball()

    # if ball in right gutter and outside right paddle position
    if ball_pos[0] > WIDTH - PAD_WIDTH - BALL_RADIUS:
        if ball_pos[1] < (paddle2_pos[1] - HALF_PAD_HEIGHT) \
                or ball_pos[1] > (paddle2_pos[1] + HALF_PAD_HEIGHT):
            # player 1 wins
            score1 += 1
            spawn_ball("LEFT")
        else:
            bounce_ball()


def bounce_ball():
    # bounce ball from paddle by switching x axis direction and increase speed
    ball_vel[0] = -ball_vel[0]
    if ball_vel[0] < 0:
        ball_vel[0] -= BALL_SPEED_INCREMENT
    else:
        ball_vel[0] += BALL_SPEED_INCREMENT


def draw(canvas):
    # global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel

    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0], [WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0], [WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update paddle's vertical position, keep paddle on the screen
    recalculate_left_paddle_position()
    recalculate_right_paddle_position()

    # update ball
    recalculate_ball_position()

    # determine whether paddle and ball collide
    check_win_conditions()

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")

    # draw paddles
    draw_left_paddle(canvas)
    draw_right_paddle(canvas)

    # draw scores
    canvas.draw_text(str(score1), (100, 100), 50, "White")
    canvas.draw_text(str(score2), (470, 100), 50, "White")


def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel[1] = -PADDLE_VEL
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel[1] = PADDLE_VEL
    if key == simplegui.KEY_MAP["w"] or key == simplegui.KEY_MAP["W"]:
        paddle1_vel[1] = -PADDLE_VEL
    if key == simplegui.KEY_MAP["s"] or key == simplegui.KEY_MAP["S"]:
        paddle1_vel[1] = PADDLE_VEL


def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["up"] or key == simplegui.KEY_MAP["down"]:
        paddle2_vel[1] = 0
    if key == simplegui.KEY_MAP["w"] \
            or key == simplegui.KEY_MAP["W"] \
            or key == simplegui.KEY_MAP["s"] \
            or key == simplegui.KEY_MAP["S"]:
        paddle1_vel[1] = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.add_button("Restart", new_game, 100)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()
