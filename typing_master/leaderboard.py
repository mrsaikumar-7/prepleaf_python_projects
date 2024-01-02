import curses
import json
def display_leaderboard(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "LEADERBOARD", curses.A_BOLD)
    
    try:
        with open('database.json', 'r') as file_obj:
            dataObj = json.load(file_obj)
            sorted_data = sorted(dataObj, key=lambda x: x['wpm'], reverse=True)

            row = 2
            for idx, entry in enumerate(sorted_data[:10]):
                leaderboard_text = f"{idx + 1}. {entry['name']}: {entry['wpm']} WPM on {entry['date']}"
                stdscr.addstr(row, 0, leaderboard_text)
                row += 1

            # Check if there's enough space to display the exit message
            if row + 2 < curses.LINES:
                stdscr.addstr(row + 2, 0, "Press any key to exit leaderboard...")
            else:
                stdscr.addstr(curses.LINES - 1, 0, "Press any key to exit leaderboard...")

        stdscr.refresh()
        stdscr.getch()
    except FileNotFoundError:
        stdscr.addstr(2, 0, "No leaderboard data available.")
        stdscr.addstr(4, 0, "Press any key to exit...")
        stdscr.refresh()
        stdscr.getch()
