import re
with open('迷宫（组诗）.pt', 'r') as file:
    lines = file.readlines()[3:]

titles = ['把池塘推向高处', '在秋天', '月亮浮在水面', '在薄雾中醒来', '暗地', '梦中狗']

prefix = ''
date = '200807'


title = ''

content = []
title_reg = re.compile(r'[⒒⒓⒔⒕⒖⒗⒘⒙⒚⒛](.*?)$')
for line in lines:
    line = line.strip()

    if '《' in line:
        if title:
            print(title)
            if prefix:
                title = prefix+'：'+title
            with open(title+'.pt', 'w')as to_w:
                to_w.writelines(
                    'title:'+title+'\r\ndate:'+date + '\r\n'+'\r\n'.join(content))

        title = line[1:-1]
        content = []
    else:
        content.append(line)
if title:
    print(title)
    if prefix:
        title = prefix+'：'+title
        with open(title+'.pt', 'w')as to_w:
            to_w.writelines(
                'title:'+title+'\r\ndate:'+date + '\r\n'+'\r\n'.join(content))
