# for display
import microbit as mb
# for start sync
import radio
# for random question selection
import random
# for sound effects
import music

# dictionary where answers will be checked
questions = {
    '2x9': 18,
    '3x8': 24,
    '4x7': 28,
    '5x6': 30,
    '6x7': 42,
    '7x7': 49,
    '7x8': 56,
    '9x9': 81,
    '4x9': 36,
    '5x8': 40
}
# Dictionary where questions will be drawn from,
# question is deleted after drawn to avoid repetition
delete_questions = {
    '2x9': 18,
    '3x8': 24,
    '4x7': 28,
    '5x6': 30,
    '6x7': 42,
    '7x7': 49,
    '7x8': 56,
    '9x9': 81,
    '4x9': 36,
    '5x8': 40
}

# number list, the index of number in this list is same
# as it's actual value, for example, numbers[0] = {image of 0}.
# this is done to cooperate with the answering mechanism
numbers = [
mb.Image(
'09900:'
'90090:'
'90090:'
'90090:'
'09900'),
mb.Image(
'00900:'
'09900:'
'00900:'
'00900:'
'09990'),
mb.Image(
'99900:'
'00090:'
'09900:'
'90000:'
'99990'),
mb.Image(
'99990:'
'00090:'
'00900:'
'90090:'
'09900'),
mb.Image(
'00990:'
'09090:'
'90090:'
'99999:'
'00090'),
mb.Image(
'99999:'
'90000:'
'99990:'
'00009:'
'99990'),
mb.Image(
'00090:'
'00900:'
'09990:'
'90009:'
'09990'),
mb.Image(
'99999:'
'00090:'
'00900:'
'09000:'
'90000'),
mb.Image(
'09990:'
'90009:'
'09990:'
'90009:'
'09990'),
mb.Image(
'09990:'
'90009:'
'09990:'
'00900:'
'09000')]

# sets the number of questions
question_num = 5

# function for getting 'yes' or 'no' input from player
def yes():
    while True:
        if mb.button_b.is_pressed():
            return True
        elif mb.button_a.is_pressed():
            return False
        mb.sleep(100)

# function for random question selection
def get_questions():
    # question list used in game process
    q_list = []
    for i in range(question_num):
        question = random.choice(list(delete_questions))
        q_list.append(question)
        # deletes question to avoid choosing it again
        del delete_questions[question]
    return q_list

# answering mechanism
def answer(question):
    num_index = 0 # this index represents the number which player is on
    ans = '' # numbers will be appended to this string
    mb.display.scroll(question)
    while True:
        if mb.button_b.is_pressed():
            # time interval added to check for button_a a bit later
            # because humans cannot press both buttons at
            # exactly the same time
            mb.sleep(100)
            # if they are both pressed, submit answer
            if mb.button_a.is_pressed():
                return int(ans)
            # if not both pressed, increase the displayed number by 1
            # or if the displayed number is 9, next number will be 0
            if num_index < 9:
                num_index += 1
            else:
                num_index = 0
        elif mb.button_a.is_pressed():
            mb.sleep(100)
            if mb.button_b.is_pressed():
                return int(ans)
            ans += str(num_index)
        mb.display.show(numbers[num_index])
        mb.sleep(150)

# game condensed into a function so it's easier to read,
# otherwise it will need to be written twice for both
# player and host
def game_process():
    # gets questions and sets starting index
    question_list = get_questions()
    question_index = 0
    # game loop so the game runs continuously
    while True:
        # check if the question is the last question, if so, go back to
        # the first question
        if question_index <= len(question_list)-1:
            # check if answer is correct
            if answer(question_list[question_index]) == questions[question_list[question_index]]:
                del question_list[question_index] # delete question if answer is correct
                # check if there are still questions left
                if len(question_list) > 0:
                    question_index += 1
                    mb.display.show(mb.Image.HAPPY)
                    music.play(music.POWER_UP)
                    mb.sleep(300)
                # if no question left, play victory music (nyan cat)
                # because microbit has a reset button, no restart
                # game mechanism is implemented
                else:
                    while True:
                        music.play(music.NYAN)
            # if wrong, go onto the next question
            else:
                question_index += 1
                mb.display.show(mb.Image.SAD)
                music.play(music.POWER_DOWN)
                mb.sleep(300)
        else:
            question_index = 0

# at the start of the game, ask whether the player is host
mb.display.scroll('H?')
if yes():
    mb.display.scroll('S?')
    if yes():
        radio.on()
        # sends starting signal
        radio.send('S')
        radio.off()
        game_process()

elif not yes():
    radio.on()
    # waits for starting signal
    while True:
        if radio.receive() == 'S':
            radio.off()
            game_process()
