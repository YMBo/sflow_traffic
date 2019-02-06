# !/usr/local/bin/python

import sys

newpath = [
    '', '/home/yangmingbo/get-traffic/venv/lib64/python27.zip',
    '/home/yangmingbo/get-traffic/venv/lib64/python2.7',
    '/home/yangmingbo/get-traffic/venv/lib64/python2.7/plat-linux2',
    '/home/yangmingbo/get-traffic/venv/lib64/python2.7/lib-tk',
    '/home/yangmingbo/get-traffic/venv/lib64/python2.7/lib-old',
    '/home/yangmingbo/get-traffic/venv/lib64/python2.7/lib-dynload',
    '/usr/lib64/python2.7', '/usr/lib/python2.7',
    '/home/yangmingbo/get-traffic/venv/lib/python2.7/site-packages'
]

sys.path += newpath
reload(sys)
