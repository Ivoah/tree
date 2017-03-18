#!/usr/bin/env python3
import os
import sys
import json

'''Python 3 remiplementation of the linux 'tree' utility'''

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

def build_tree(dir, opts, top = True):
    dirs = 0
    files = 0

    if top:
        contents, dirs, files = build_tree(dir, opts, False)
        return [
            {
                'name': dir,
                'type': 'directory',
                'contents': contents
            },
            {
                'type': 'report',
                'directories': dirs,
                'files': files
            }
        ]
    else:
        tree = []
        dirs = 0
        files = 0

        for filename in sorted(os.listdir(dir), key = str.lower):
            if filename[0] == '.': continue
            path = os.path.join(dir, filename)
            node = {
                'name': filename,
                'size': os.path.getsize(path)
            }
            if os.path.isdir(path):
                node['type'] = 'directory'
                node['contents'], d, f = build_tree(path, opts, False)
                dirs += d
                files += f
            else:
                node['type'] = 'file'
                files += 1
            tree.append(node)
        return tree, dirs, files

def print_tree(tree, opts):
    pass

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
            print(pre + strs[2 if 1 == dir_len else 1] + colorize(path))
            if os.path.islink(path):
                dirs += 1
            else:
                d, f, s = print_dir(path, pre + strs[3 if i == dir_len else 0], opts = opts)
                dirs += d + 1
                files += f
                size += s
        else:
            files += 1
            size += os.path.getsize(path)
            print(pre + strs[2 if i == dir_len else 1] + ('[{:>11}]  '.format(size) if opts['show_size'] else '') + colorize(path))

    return (dirs, files, size)

dirs = 0
files = 0

opts = {
    'show_hidden': False,
    'show_size': False,
    'follow_symlinks': False
}

tree = build_tree('.', opts)
print(json.dumps(tree, sort_keys = True))
