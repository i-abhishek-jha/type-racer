import curses  # Used for creating terminal-based UI
from curses import wrapper
import time
import random
from text import sentences  # Import predefined sentences from an external file


# Display the start screen with instructions
def start_scree(stdscr):
    stdscr.clear()
    stdscr.addstr("Type Racer")
    stdscr.addstr("\nPress any key to begin!")
    stdscr.refresh()
    stdscr.getkey()

# Display the target text, user's input, and WPM on the screen
def dispaly_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM: {wpm}")

    # Highlight the typed characters, showing correct and incorrect in different colors
    for i, char in enumerate(current):
            correct_char = target[i]
            color = curses.color_pair(1)
            if char != correct_char:
                color = curses.color_pair(2)

            stdscr.addstr(0, i, char, color)

# Load a random sentence from the `sentences` list
def load_text():
    lines = random.choice(sentences)
    return lines

# Main typing test logic
def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        # Calculate elapsed time and WPM
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        stdscr.clear()
        dispaly_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        # Check if the user has completed typing the target text
        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break
        
        try:
            key = stdscr.getkey()
        except:
            continue

        # Handle escape key to exit
        if ord(key) == 27:
            break

        # Handle backspace to delete the last character
        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if len(current_text) > 0:
                current_text.pop()

        elif len(current_text) < len(target_text):
            current_text.append(key)


# Main function to initialize the curses environment and start the program
def main(stdscr):
    # Initialize color pairs for correct and incorrect.
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    
    start_scree(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr(2, 0, "You complated the text! Press any key to continue...")
        key = stdscr.getkey()

        if ord(key) == 27:
            break

# Wrapper function to handle curses setup and teardown
wrapper(main)