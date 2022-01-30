#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import random
import io
import codecs
import curses

TABLE_SIZE = 5
WORDS_FILENAME = 'words.it.txt'

def has_color_support(stream):
    """Try to determine if the given stream supports colored output.

    Return True only if the stream declares to be a TTY, if it has a
    file descriptor on which ncurses can initialize a terminal and if
    that terminal's entry in terminfo declares support for colors.

    stream (fileobj): a file-like object (that adheres to the API
        declared in the `io' package).

    return (bool): True if we're sure that colors are supported, False
        if they aren't or if we can't tell.

    """
    if stream.isatty():
        try:
            curses.setupterm(fd=stream.fileno())
            # See `man terminfo` for capabilities' names and meanings.
            if curses.tigetnum("colors") > 0:
                return True
        # fileno() can raise IOError or OSError (since Python 3.3).
        except Exception:
            pass
    return False

def add_color_to_string(string, color, stream=sys.stdout, bold=False,
                        force=False):
    """Format the string to be printed with the given color.

    Insert formatting characters that, when printed on a terminal, will
    make the given string appear with the given foreground color if the
    stream passed has color support. Else return the string as it is.

    string (string): the string to color.
    color (int): the color as a colors constant, like colors.BLACK.
    stream (fileobj): a file-like object (that adheres to the API
        declared in the `io' package). Defaults to sys.stdout.
    bold (bool): True if the string should be bold.
    force (bool): True if the string should be formatted even if the
        given stream has no color support.

    return (string): the formatted string.

    """
    if force or has_color_support(stream):
        return (curses.tparm(curses.tigetstr("setaf"), color) if color != curses.COLOR_BLACK else b'') + \
            (curses.tparm(curses.tigetstr("bold")) if bold else b'') + \
            string.encode('utf-8') + \
            curses.tparm(curses.tigetstr("sgr0"))
    else:
        return string.encode('utf-8')

class Game:
    def __init__(self, chosen, max_word_len):
        self.chosen = chosen
        self.max_word_len = max_word_len

        self.word_format = "{:^%d}" % (max_word_len)
        self.colors = [curses.COLOR_WHITE] * len(self.chosen)

    def print_table(self):
        sys.stdout.buffer.write(((b'+' + b'-' * (self.max_word_len+2)) * TABLE_SIZE) + b'+\n')
        for i in range(TABLE_SIZE):
            sys.stdout.buffer.write(((b'|' + b' ' * (self.max_word_len+2)) * TABLE_SIZE) + b'|\n')
            for j in range(TABLE_SIZE):
                sys.stdout.buffer.write(b'| ')
                sys.stdout.buffer.write(add_color_to_string(self.word_format.format(self.chosen[i+TABLE_SIZE*j]), color=self.colors[i+TABLE_SIZE*j], bold=True))
                sys.stdout.buffer.write(b' ')
            sys.stdout.buffer.write(b'|\n')
            for j in range(TABLE_SIZE):
                sys.stdout.buffer.write(((b'|' + ' {},{}'.format(i+1, j+1).encode('utf8') + b' ' * (self.max_word_len+2-4))))
            sys.stdout.buffer.write(b'|\n')
            sys.stdout.buffer.write(((b'+' + b'-' * (self.max_word_len+2)) * TABLE_SIZE) + b'+\n')
        sys.stdout.buffer.flush()

    def get_word_and_colour(self, i, j):
        return self.chosen[i+TABLE_SIZE*j], self.colors[i+TABLE_SIZE*j]

    def set_colour(self, i, j, colour):
        if colour.startswith('r'):
            self.colors[i+TABLE_SIZE*j] = curses.COLOR_RED
        elif colour.startswith('b'):
            self.colors[i+TABLE_SIZE*j] = curses.COLOR_BLUE
        elif colour.startswith('y'):
            self.colors[i+TABLE_SIZE*j] = curses.COLOR_YELLOW
        elif colour.startswith('w'):
            self.colors[i+TABLE_SIZE*j] = curses.COLOR_WHITE
        else:
            return False
        return True

def main():
    with io.open(WORDS_FILENAME, encoding='utf-8') as fin:
        words = [x.strip() for x in fin.readlines()]
    max_word_len = max([len(x) for x in words])
    random.seed()
    chosen = random.sample(words, TABLE_SIZE * TABLE_SIZE)
    game = Game(chosen, max_word_len)
    while True:
        game.print_table()
        sys.stdout.write("Command? ")
        command = sys.stdin.readline().strip().lower()
        if command == 'quit' or command == 'exit':
            break
        else:
            wrong = False
            try:
                (i, j) = [int(x.strip())-1 for x in command.split(',')]
            except ValueError:
                wrong = True
            else:
                if not(0 <= i <= TABLE_SIZE-1 and 0 <= j <= TABLE_SIZE-1):
                    wrong = True
            if wrong:
                sys.stdout.write("Wrong position\n")
                continue
            word, colour = game.get_word_and_colour(i, j)
            sys.stdout.write("Current word is {}. What is the new colour? ".format(add_color_to_string(word, color=colour, bold=True)))
            new_colour = sys.stdin.readline().strip().lower()
            ret = game.set_colour(i, j, new_colour)
            if not ret:
                sys.stdout.write("Colour unknown!\n")

if __name__ == '__main__':
    main()
