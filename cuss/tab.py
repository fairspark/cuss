import curses

class Tab:

    def __init__(self, header):
        self._init_border_types()
        self._header = header
        self._height = curses.LINES-3
        self._width = curses.COLS
        self._start_row = 2
        self._start_col = 0
        self.window = curses.newwin(self._height, self._width, self._start_row, self._start_col)
        self.subwindow = self.window.subwin(self._height-2, self._width-2, 2,1)
        self.window.border(*self.border_types['box_top_open'])


    def _init_border_types(self):
        self.border_types = {
                'box_top_open':[0,0,' ',0,curses.ACS_VLINE,curses.ACS_VLINE,0,0]
                }


    def update(self):
        self.subwindow.addstr(2,2,self._header + ' selected!')
        self.window.noutrefresh()
        self.subwindow.noutrefresh()

    def get_header(self):
        return self._header



