import os
import sys

filename = 'last_color_purple.py'
if not os.path.exists(filename):
    print('文件不存在')
    sys.exit()
print('读文件')
with open(filename, 'r', encoding='utf-8') as f:
    line_list = f.readlines()

need_read = False
last_line = []
for i, line in enumerate(line_list):
    if 'setStyleSheet' in line:
        last_line.append(line)
        if line.endswith('")\n'):
            need_read = False
        else:
            need_read = True
        continue
    if need_read:
        last_line.append(line)
        if line.endswith('")\n'):
            need_read = False
        else:
            need_read = True
print('查找完毕')
with open('last_line.txt', 'w') as f:
    for line in last_line:
        print(line)
        f.write(line)
