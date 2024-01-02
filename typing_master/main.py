import  curses
from curses import wrapper
import time
import requests, json
from datetime import date
from leaderboard import display_leaderboard
import random
        
        
def get_user_input(stdscr, prompt_string):
    curses.echo()  # Enable echoing of input
    stdscr.clear()
    stdscr.addstr(0, 0, prompt_string)
    stdscr.refresh()
    user_input = stdscr.getstr().decode(encoding="utf-8")
    curses.noecho()  # Disable echoing of input
    return user_input

def start_screen(stdscr):
  stdscr.clear()
  stdscr.addstr(0, 0, "Welcome to the speed typing test!", curses.A_BOLD)
  stdscr.addstr("\nPress any key to begin")
  stdscr.refresh()  
  stdscr.getkey()

def display_text(stdscr, target, current, wpm=0):
    max_width = min(len(target), curses.COLS - 1)  # Limit width to screen width - 1
    stdscr.addstr(0, 0, target[:max_width])  # Display the portion that fits
    stdscr.addstr(1, 0, f"WPM: {wpm}", curses.A_BOLD)
    
    for i, c in enumerate(current[:max_width]):  # Loop through characters within the width
        correct_char = target[i]
        color = curses.color_pair(1) if c == correct_char else curses.color_pair(2)
        stdscr.addstr(0, i, c, color)


def load_text():
    with open('quotes.txt', 'r') as file:
        lines = file.readlines()
        return random.choice(lines).strip()  # Select a random line and remove leading/trailing spaces


def wpm_test(stdscr):
  target_text = load_text()
  current_text = []
  wpm = 0
  username = get_user_input(stdscr, "Enter your name: ")
  start_time = time.time()
  stdscr.nodelay(True)
  
  while True:
    time_elapsed = max(time.time() - start_time, 1)
    wpm = round((len(current_text) / (time_elapsed / 60)) / 5)
    
    stdscr.clear()
    display_text(stdscr, target_text, current_text, wpm)
    
    stdscr.refresh()
    
    if "".join(current_text) == target_text:
      stdscr.nodelay(False)
      break
    
    try:
      key = stdscr.getkey()
    except:
      continue
    
    if ord(key) == 27:
      break
    if key in ("KEY_BACKSPACE", "\b", "\x7f"):
      if len(current_text) > 0:
        current_text.pop()
    elif len(current_text) < len(target_text):
      current_text.append(key)
  
  my_dict = {
    'name': username,
    'wpm': wpm,
    'date': date.today().strftime("%b-%d-%Y")
  }
  with open('database.json', 'r') as file_obj:
    dataObj = json.load(file_obj)
  
  dataObj.append(my_dict)
  with open('database.json', 'w') as json_file:
    json.dump(dataObj, json_file, indent=4, separators=(',', ': '))
  
    

def main(stdscr):
  curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
  curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
  curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
  
  start_screen(stdscr)
  while True:
    wpm_test(stdscr)
    
    stdscr.addstr(2, 0, "You've completed the text! Press any key to continue or escape to get out...")
    key = stdscr.getkey()
    if ord(key) == 27:
      display_leaderboard(stdscr)  
      break

wrapper(main)