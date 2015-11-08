try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


# define global variables
tenths_of_seconds = 0
guesses, tries = 0, 0
timer_already_stopped = False


# receives an int value as input
# if val is lower than 10, add a leading zero
# return result as string
def add_leading_zero(val):
    result = str(val)
    if val < 10:
        result = "0" + result
    return result


# converts time in tenths of seconds into formatted string A:BC.D
def format_canvas_text(val):
    tenths_of_second = val % 10
    val = (val - tenths_of_second) / 10
    seconds = val % 60
    val = (val - seconds) / 60
    minutes = val

    return str(minutes) + \
        ":" + add_leading_zero(seconds) + \
        "." + str(tenths_of_second)


# define event handlers for buttons; "Start", "Stop", "Reset"
def start_stopwatch():
    global stopwatch_timer, timer_already_stopped
    stopwatch_timer.start()
    timer_already_stopped = False


def stop_stopwatch():
    global stopwatch_timer, guesses, tries, timer_already_stopped
    stopwatch_timer.stop()
    if not timer_already_stopped:
        tries += 1
        if (tenths_of_seconds % 10) == 0:
            guesses += 1
    timer_already_stopped = True


def reset_stopwatch():
    global stopwatch_timer, tenths_of_seconds, guesses, tries, timer_already_stopped
    stopwatch_timer.stop()
    timer_already_stopped = False
    tenths_of_seconds, guesses, tries = 0, 0, 0


# define event handler for timer with 0.1 sec interval
def increment_stopwatch():
    global tenths_of_seconds
    tenths_of_seconds += 1


# define draw handler
def draw(canvas):
    # draw stopwatch value
    canvas.draw_text(format_canvas_text(tenths_of_seconds), (70, 170), 60, 'White')
    # draw guesses and tries
    val = str(guesses) + "/" + str(tries)
    canvas.draw_text(val, (230, 30), 30, 'Red')

# create frame
frame = simplegui.create_frame("Stopwatch", 300, 300)
stopwatch_timer = simplegui.create_timer(100, increment_stopwatch)

# register event handlers
frame.add_button("Start", start_stopwatch, 100)
frame.add_button("Stop", stop_stopwatch, 100)
frame.add_button("Reset", reset_stopwatch, 100)
frame.set_draw_handler(draw)

# start frame
frame.start()
