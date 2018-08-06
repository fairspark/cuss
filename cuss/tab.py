import curses

class Tab:

    def __init__(self, header, height, width):
        self._init_border_types()
        self._header = header
        self._set_size(height, width)
        self._start_row = 2
        self._start_col = 0

        self.update(self._width, self._height)


    def _set_size(self, height, width):
        self._width = width
        self._height = height-3


    def _init_border_types(self):
        self.border_types = {
                'box_top_open':[0,0,' ',0,curses.ACS_VLINE,curses.ACS_VLINE,0,0]
                }


    def update(self, height, width):
        self._set_size(height, width)

        # Create boxed tab-window and subwindow
        self.window = curses.newwin(self._height, self._width, self._start_row, self._start_col)
        self.window.addstr(10,2, 'tab height ' + str(self._height))
        self.subwindow = self.window.subwin(self._height-2, self._width-2, 2,1)
        self.window.border(*self.border_types['box_top_open'])

        self.subwindow.addstr(2,2,self._header + ' selected!')
        self.window.noutrefresh()
        self.subwindow.noutrefresh()


    def get_header(self):
        return self._header



