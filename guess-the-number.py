try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

# initialize with [0, 100) range and 7 allowed guesses
min_guess_range, max_guess_range, allowed_guesses = 0, 100, 7
player_guesses = 0
secret_number = 0


# helper function to start and restart the game
def new_game():
    global secret_number, player_guesses
    secret_number = random.randrange(min_guess_range, max_guess_range)
    player_guesses = 0
    print
    print "Starting a new game in the [" \
          + str(min_guess_range) \
          + "," \
          + str(max_guess_range) \
          + ") range"


# define event handlers for control panel
def range100():
    global min_guess_range, max_guess_range, allowed_guesses
    min_guess_range, max_guess_range, allowed_guesses = 0, 100, 7
    new_game()


def range1000():
    global min_guess_range, max_guess_range, allowed_guesses
    min_guess_range, max_guess_range, allowed_guesses = 0, 1000, 10
    new_game()


def input_guess(guess):
    global player_guesses

    guess = int(guess)
    print "Your guess was", str(guess)

    if guess == secret_number:
        print "Correct, you win!!!"
        new_game()
    elif guess > secret_number:
        print "Lower"
        player_guesses += 1
    else:
        print "Higher"
        player_guesses += 1

    if player_guesses < allowed_guesses:
        print "You have", str(allowed_guesses - player_guesses), "guesses left"
    else:
        print "You have ran out of guesses, you lose!"
        new_game()


# create frame
f = simplegui.create_frame("Guess the number", 200, 200)
f.add_button("Range 0 - 100", range100, 100)
f.add_button("Range 0 - 1000", range1000, 100)
f.add_input("Guess the number", input_guess, 50)

# register event handlers for control elements and start frame
f.start()

# call new_game
new_game()
