from tab import *
from standardscreen import *
from curses import wrapper


def main(stdscr):
    screen = StandardScreen()
    screen.display()



if __name__ == '__main__':
    wrapper(main)


