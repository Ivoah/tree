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

def print_dir(dir, pre = '', opts = {}):
    dirs = 0
    files = 0
    size = 0

    if pre == '': print(colors.dir + dir + colors.end)

    dir_len = len(os.listdir(dir)) - 1
    for i, file in enumerate(sorted(os.listdir(dir), key = str.lower)):
        path = os.path.join(dir, file)
        if file[0] == '.' and not opts['show_hidden']: continue
        if os.path.isdir(path):
            print(pre + strs[2 if i == dir_len else 1] + colorize(path))
            if os.path.islink(path):
                dirs += 1
            else:
                d, f, s = print_dir(path, pre + strs[3 if i == dir_len else 0], opts = opts)
                dirs += d + 1
                files += f
                size += s
        else:
            files += 1
            size += os.path.getsize(path)
            print(pre + strs[2 if i == dir_len else 1] + ('[{:>11}]  '.format(size) if opts['show_size'] else '') + colorize(path))


    return (dirs, files, size)

dirs = 0
files = 0

opts = {
    'show_hidden': False,
    'show_size': False,
    'follow_symlinks': False
}

if len(sys.argv) == 1:
    dirs, files, size = print_dir('.', opts = opts)
else:
    for dir in sys.argv[1:]:
        d, f = print_dir(dir, opts = opts)
        dirs += d
        files += f

print()
print('{} director{}, {} file{}'.format(dirs, 'ies' if dirs != 1 else 'y', files, 's' if files != 1 else ''))
