#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPLv3 Copyright: 2020, Kovid Goyal <kovid at kovidgoyal.net>

import os
import shlex
import subprocess
import sys


def run(*a):
    if len(a) == 1:
        a = shlex.split(a[0])
    print(' '.join(map(shlex.quote, a)))
    ret = subprocess.Popen(a).wait()
    if ret != 0:
        raise SystemExit(ret)


def install_deps():
    print('Installing kitty dependencies...')
    run('apt-get update')
    run('apt-get install -y libgl1-mesa-dev libxi-dev libxrandr-dev libxinerama-dev'
        ' libxcursor-dev libxcb-xkb-dev libdbus-1-dev libxkbcommon-dev libharfbuzz-dev'
        ' libpng-dev libfontconfig-dev libxkbcommon-x11-dev libcanberra-dev')
    run('pip install Pillow flake8 pygments')


def build_kitty():
    cmd = 'python setup.py build --debug --verbose'
    if 'KITTY_SANITIZE' in os.environ:
        cmd += ' --sanitize'
        os.environ['ASAN_OPTIONS'] = 'leak_check_at_exit=0'
    run(cmd)


def test_kitty():
    run('./kitty/launcher/kitty +launch test.py')


def package_kitty():
    run('python setup.py linux-package --update-check-interval=0')


def main():
    action = sys.argv[-1]
    if action in ('build', 'package'):
        install_deps()
    if action == 'build':
        build_kitty()
    elif action == 'package':
        package_kitty()
    elif action == 'test':
        test_kitty()
    else:
        raise SystemExit('Unknown action: ' + action)


if __name__ == '__main__':
    main()
