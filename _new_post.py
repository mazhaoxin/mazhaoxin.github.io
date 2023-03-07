# Generate new post template
# MaZhaoxin @20230307

post_path = r'mazhaoxin.github.io/_posts'
typora_path = r'C:/"Program Files"/Typora/Typora.exe'

print('# Generate new post template')
title = input('title: ').strip()
slug = input('slug (filename): ').strip().replace(' ', '_')
tags = input('tags: ').strip()
header_img = input('header_img [coding, comm, ic, manager, matlab, pll, thinking]: ').strip()

from datetime import datetime
dt = datetime.now().strftime('%Y-%m-%d %H:%M') # yyyy-mm-dd HH:MM
fname = datetime.now().strftime(f'%Y-%m-%d-{slug}.md')

s = f'''---
typora-root-url: ..
layout: post
title: "{title}"
date: {dt}
author: "MaZhaoxin"
header-img: "img/bg-post/{header_img}.jpg"
catlog: true
tags:
'''

for tag in tags.split():
    if tag.strip() != '':
        s += f"    - {tag}\n"
s+= '---\n\n'


print('\n')
print(fname)
print('#'*50)
print(s)

print('#'*50)
print()
print('Note: ')
print('  - 图片需要手动移动到/img/in-post/目录下；')
print('  - 并修改md文件中的路径（增加"/img/in-post/"）；')
print()
print('#'*50)
print()

if input('OK? [y/n]: ').strip().lower() == 'y':
    with open(f'{post_path}\{fname}', mode='w', encoding='utf-8') as f:
        f.write(s)
        
import os
cwd = os.getcwd().replace('\\', '/')
# os.system(f'{typora_path} {cwd}/{post_path}/{fname}')
os.system(f'start {cwd}/{post_path}/{fname}') # looks good!
