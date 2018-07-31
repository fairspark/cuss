import curses
from tab import *

class StandardScreen:
    _tabs = []
    _tab_headers = []

    def __init__(self):
        self.stdscr = curses.initscr()
        self.stdscr.keypad(1)

        # Properly initialize the screen
        curses.noecho()
        curses.cbreak()         # Intercepts keystrokes
        curses.curs_set(0)      # Hide cursor

        self._enable_color()
        self._init_colors()
        self._init_title()
        self._init_footer()
        self._add_tabs()


    def __del__(self):
        # Restore the terminal settings
        self.stdscr.keypad(0)
        curses.nocbreak()
        curses.echo()
        curses.curs_set(1)

        # Retore the terminal itself to its "former glory"
        curses.endwin()
    


    def _init_colors(self):
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)


    def _enable_color(self):
        if curses.has_colors():
            curses.start_color()


    def _init_title(self):
        self.title = "CUSS - Common Unix-like SNMP Station"
        self.stdscr.addstr(self.title, curses.A_REVERSE)
        self.stdscr.chgat(-1, curses.A_REVERSE)


    def _init_footer(self):
        self.stdscr.addstr(curses.LINES-1, 0, " Press 'Q' to quit")

        # Change the Q to green
        self.stdscr.chgat(curses.LINES-1, 8, 1, curses.A_BOLD | curses.color_pair(1))


    def _add_tabs(self):
        self._tabs.append(Tab("Dashboard"))
        self._tabs.append(Tab("CPU"))
        self._tabs.append(Tab("Memory"))
        self._tabs.append(Tab("Network"))
        self._tabs.append(Tab("Updates"))
        self._tabs.append(Tab("Config"))
        self._active_index = 0
        self._active_tab = self._tabs[self._active_index]
        self._update_tab_headers()
        self.update()


    def _update_tab_headers(self):
        # Generate a list of tab headers from each of their corresponding titles
        tab_headers = []
        for tab in self._tabs:
            tab_headers.append(tab.get_header())

        self._tab_headers = tab_headers

    

    def tab_shift_right(self):
        if self._active_index < len(self._tabs) - 1:
            self._active_index = self._active_index + 1
            self._active_tab = self._tabs[self._active_index]


    def tab_shift_left(self):
        if self._active_index > 0:
            self._active_index = self._active_index - 1
            self._active_tab = self._tabs[self._active_index]
            

    def update(self):

        self.stdscr.addch(1,0,curses.ACS_ULCORNER )

        # Draw horizontal bar
        for x in range(curses.COLS-2):
            self.stdscr.addch(curses.ACS_HLINE)
        self.stdscr.addch(1,curses.COLS-1,curses.ACS_URCORNER )

        # Set cursor
        tab_offsets = 3
        self.stdscr.addstr(1, tab_offsets, ' ')

        # Draw tab headers
        for header in self._tab_headers:
            if (header == self._active_tab.get_header()):
                self.stdscr.addstr(header, curses.A_BOLD|curses.A_REVERSE)
                self.stdscr.addstr(' ')
            else:
                self.stdscr.addstr(header + ' ')


        #self.stdscr.addstr(1, tab_offsets, tab_header_str)
        self.stdscr.noutrefresh()
        self._active_tab.update()
        curses.doupdate()


    def display(self):
        # Create the event loop
        while True:
            #c = tab.getch()
            c = self.stdscr.getch()

            # TODO - Handle various keystrokes here
            if c == curses.KEY_RIGHT:
                self.tab_shift_right()
            elif c == curses.KEY_LEFT:
                self.tab_shift_left()
            elif c == ord('q') or c == ord('Q'):
                break

            # Refresh subwindow
            self._active_tab.subwindow.clear()
            self._active_tab.subwindow.refresh()

            # Refresh the windows from the bottom up
            self.update()
            curses.doupdate()
