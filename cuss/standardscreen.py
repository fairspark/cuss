import curses
from tab import *

class StandardScreen:
    _tabs = []
    _tab_headers = []


    # Private methods
    def __init__(self):
        self.stdscr = curses.initscr()
        self.stdscr.keypad(1)

        # Properly initialize the screen
        curses.noecho()
        curses.cbreak()         # Intercepts keystrokes
        curses.curs_set(0)      # Hide cursor

        self._height = curses.LINES
        self._width = curses.COLS
        self._enable_color()
        self._init_colors()
        self._init_tabs()
        self._set_active_tab(0)
        self.update()


    def __del__(self):
        # Restore the terminal settings
        self.stdscr.keypad(0)
        curses.nocbreak()
        curses.echo()
        curses.curs_set(1)
        curses.endwin()


    def resize(self):
        resize = curses.is_term_resized(self._height, self._width)
        
        if resize is True:
            y, x = self.stdscr.getmaxyx()
            self.stdscr.addstr(2,2, str(x))


    def _init_colors(self):
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)


    def _enable_color(self):
        if curses.has_colors():
            curses.start_color()


    def _init_title(self):
        self.title = "CUSS - Common Unix-like SNMP Station"
        self.stdscr.addstr(0,0,self.title, curses.A_REVERSE)
        self.stdscr.chgat(-1, curses.A_REVERSE)


    def _init_footer(self):
        self.stdscr.addstr(curses.LINES-1, 0, " Press 'Q' to quit")

        # Change the Q to green
        self.stdscr.chgat(curses.LINES-1, 8, 1, curses.A_BOLD | curses.color_pair(1))


    def _set_active_tab(self, index):
        self._active_index = index
        self._active_tab = self._tabs[index]


    def _init_tabs(self):
        self._tabs.append(Tab("Dashboard", self._height, self._width))
        self._tabs.append(Tab("CPU", self._height, self._width))
        self._tabs.append(Tab("Memory", self._height, self._width))
        self._tabs.append(Tab("Network", self._height, self._width))
        self._tabs.append(Tab("Updates", self._height, self._width))
        self._tabs.append(Tab("Config", self._height, self._width))
        self._init_tab_headers()


    def _init_tab_headers(self):
        # Generate a list of tab headers from each of their corresponding titles
        tab_headers = []
        for tab in self._tabs:
            tab_headers.append(tab.get_header())

        self._tab_headers = tab_headers


    def _draw_line_header(self):
        # Draw upper left corner
        self.stdscr.addch(1,0,curses.ACS_ULCORNER )

        # Draw upper horizontal bar
        for x in range(self._width - 2):
            self.stdscr.addch(curses.ACS_HLINE)

        # Draw upper right corner
        self.stdscr.addch(curses.ACS_URCORNER)


    def _print_headers(self):
        active_header = self._active_tab.get_header()

        # Set cursor
        tab_offsets = 3
        self.stdscr.addstr(1, tab_offsets, ' ')

        # Draw tab headers
        for header in self._tab_headers:
            if (header ==  active_header):
                self.stdscr.addstr(header, curses.A_BOLD|curses.A_REVERSE)
                self.stdscr.addstr(' ')
            else:
                self.stdscr.addstr(header + ' ')


    # Public methods
    def tab_shift_right(self):
        total_tabs = len(self._tabs)

        if self._active_index < (total_tabs - 1):
            self._active_index += 1
            self._active_tab = self._tabs[self._active_index]


    def tab_shift_left(self):
        if self._active_index > 0:
            self._active_index -= 1
            self._active_tab = self._tabs[self._active_index]
            

    def update(self):
        self.stdscr.clear()
        self._init_title()
        self._draw_line_header()
        self._print_headers()
        self._init_footer()
        self.stdscr.noutrefresh()
        self.stdscr.addstr(7,2, 'self._height ' + str(self._height))
        self.stdscr.addstr(8,2, 'self._width  ' + str(self._width))
        self.stdscr.addstr(9,2, 'curses.LINES ' + str(curses.LINES))
        self.stdscr.addstr(10,2, 'curses.COLS  ' + str(curses.COLS))
        self._active_tab.update(self._height, self._width)
        curses.doupdate()


    def display(self):
        # Display event loop
        while True:
            y, x = self.stdscr.getmaxyx()
            if( y != self._height ) or ( x != self._width ):
                self._height = y
                self._width = x
                curses.resizeterm(y, x)
                self.update()

            c = self.stdscr.getch()
            

            # TODO - Handle various keystrokes here
            if c == curses.KEY_RIGHT:
                self.tab_shift_right()
#            elif c == curses.KEY_RESIZE:
#                self.resize()
            elif c == curses.KEY_LEFT:
                self.tab_shift_left()
            elif c == ord('q') or c == ord('Q'):
                break

            # Refresh subwindow
            self._active_tab.subwindow.clear()
            self._active_tab.subwindow.refresh()

            # Refresh the windows from the bottom up
            self.update()


