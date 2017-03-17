#!/usr/bin/env python3

'''Python 3 remiplementation of the linux 'tree' utility'''

import os
import sys

chars = {
    'nw': '\u2514',
    'nws': '\u251c',
    'ew': '\u2500',
    'ns': '\u2502'
}

strs = [
    chars['ns'] + '   ',
    chars['nws'] + chars['ew']*2 + ' ',
    chars['nw'] + chars['ew']*2 + ' ',
    '    '
]

class colors:
    dir = '\033[01;34m'
    exec = '\033[01;32m'
    link = '\033[01;36m'
    deadlink = '\033[40;31;01m'
    end = '\033[00m'

def colorize(path, full = False):
    file = path if full else os.path.basename(path)

    if os.path.islink(path):
        return colors.link + file + colors.end + ' -> ' + colorize(os.readlink(path), True)

    if os.path.isdir(path):
        return colors.dir + file + colors.end

    if os.access(path, os.X_OK):
        return colors.exec + file + colors.end

    return file

def print_dir(dir, pre = ''):
    dirs = 0
    files = 0

    if pre == '': print(colors.dir + dir + colors.end)

    dir_len = len(os.listdir(dir)) - 1
    for i, file in enumerate(sorted(os.listdir(dir), key = str.lower)):
        path = os.path.join(dir, file)
        if file[0] == '.': continue
        print(pre + strs[2 if i == dir_len else 1] + colorize(path))
        if os.path.isdir(path):
            if os.path.islink(path):
                dirs += 1
            else:
                d, f = print_dir(path, pre + strs[3 if i == dir_len else 0])
                dirs += d + 1
                files += f
        else:
            files += 1

    return (dirs, files)

dirs = 0
files = 0

if len(sys.argv) == 1:
    dirs, files = print_dir('.')
else:
    for dir in sys.argv[1:]:
        d, f = print_dir(dir)
        dirs += d
        files += f

print()
print('{} director{}, {} file{}'.format(dirs, 'ies' if dirs != 1 else 'y', files, 's' if files != 1 else ''))
