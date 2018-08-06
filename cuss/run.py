from tab import *
from standardscreen import *
from curses import wrapper


def main(stdscr):
    screen = StandardScreen()
    screen.addtitlebar('CUSS - Common Unix-like SNMP Station')
    screen.display()



if __name__ == '__main__':
    wrapper(main)


