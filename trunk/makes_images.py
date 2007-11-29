#!/usr/bin/env python
import os

for pos in range(8):
    for num in range(10):
        os.system('cp num-up-%d.gif num-up-%d-%d.gif' % (num, pos, num))
        os.system('cp num-down-%d.gif num-down-%d-%d.gif' % (num, pos, num))
