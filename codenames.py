#!/usr/bin/env python2

import sys
import random

TABLE_SIZE = 5
WORDS_FILENAME = 'words.it.txt'

def main():
    with open(WORDS_FILENAME) as fin:
        words = [x.strip() for x in fin.readlines()]
    max_word_len = max([len(x) for x in words])
    word_format = "| %%%ds " % (max_word_len)
    random.seed()
    chosen = random.sample(words, TABLE_SIZE * TABLE_SIZE)
    sys.stdout.write((('+' + '-' * (max_word_len+2)) * TABLE_SIZE) + '+\n')
    for i in xrange(TABLE_SIZE):
        sys.stdout.write((('|' + ' ' * (max_word_len+2)) * TABLE_SIZE) + '|\n')
        for j in xrange(TABLE_SIZE):
            sys.stdout.write(word_format % (chosen[i+TABLE_SIZE*j]))
        sys.stdout.write('|\n')
        sys.stdout.write((('|' + ' ' * (max_word_len+2)) * TABLE_SIZE) + '|\n')
        sys.stdout.write((('+' + '-' * (max_word_len+2)) * TABLE_SIZE) + '+\n')

if __name__ == '__main__':
    main()
