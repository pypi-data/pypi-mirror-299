"""xkbid - x keyboard id"""
# -*- encoding: utf-8 -*-

from os import name as osname

from platform import system

from subprocess import Popen, PIPE, DEVNULL

if osname == 'nt' or system() == 'Windows':
    def xkbid(*_): pass
else:
    def xkbid(name='keyboard'):
        o, e = Popen('xinput', stdout=PIPE, stderr=DEVNULL, shell=True).communicate()
        if o:
            o = o.decode()
        if e:
            e = e.decode()
        lns = [l for l in o.split('\n')]
        lns = [l for l in lns if l]
        hlns = [l for l in lns if name and name.lower() in l.lower()]
        kbln = lns[-1] if not hlns else hlns[-1]
        kbln = int(kbln.split('=')[1].split()[0])
        return kbln
