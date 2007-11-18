import os

for num in range(10):
  for pos in range(8):
    os.system('cp num-%d.gif num-%d-%d.gif' % (num, pos, num))
