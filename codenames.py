#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
import random
import io
import codecs

TABLE_SIZE = 5
WORDS_FILENAME = 'words.it.txt'

def main():
    sys.stdout = codecs.getwriter('utf8')(sys.stdout)
    with io.open(WORDS_FILENAME, encoding='utf-8') as fin:
        words = [x.strip() for x in fin.readlines()]
    max_word_len = max([len(x) for x in words])
    word_format = "| {:^%d} " % (max_word_len)
    random.seed()
    chosen = random.sample(words, TABLE_SIZE * TABLE_SIZE)
    sys.stdout.write((('+' + '-' * (max_word_len+2)) * TABLE_SIZE) + '+\n')
    for i in xrange(TABLE_SIZE):
        sys.stdout.write((('|' + ' ' * (max_word_len+2)) * TABLE_SIZE) + '|\n')
        for j in xrange(TABLE_SIZE):
            sys.stdout.write(word_format.format(chosen[i+TABLE_SIZE*j]))
        sys.stdout.write('|\n')
        sys.stdout.write((('|' + ' ' * (max_word_len+2)) * TABLE_SIZE) + '|\n')
        sys.stdout.write((('+' + '-' * (max_word_len+2)) * TABLE_SIZE) + '+\n')

if __name__ == '__main__':
    main()
