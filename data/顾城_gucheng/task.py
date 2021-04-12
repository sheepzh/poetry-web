import re
with open('歌乐山诗组（四首）.pt', 'r') as file:
    lines = file.readlines()[3:]

titles = ['谋杀', '挣扎', '死灭','小萝卜头和鹿']

prefix = '歌乐山诗组'
date = '1979'


title = ''

content = []
title_reg = re.compile(r'^\d{1,2}.\s(.*)$')
for line in lines:
    line = line.strip()

    if line in titles:
        if title:
            print(title)
            if prefix:
                title = prefix+'：'+title
            with open(title+'.pt', 'w')as to_w:
                to_w.writelines(
                    'title:'+title+'\r\ndate:'+date + '\r\n'+'\r\n'.join(content))

        title = line
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
