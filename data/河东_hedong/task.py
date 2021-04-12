import re
with open('五月，像小麦一样弯下腰去（组诗）.pt', 'r') as file:
    lines = file.readlines()[3:]

titles = ['我没有江湖', '路找到了我', '运输自己', '麦子', '暗地', '梦中狗']

prefix = '五月，像小麦一样弯下腰去'
date = '200810'

title_reg = re.compile(r'^〇(.*)$')

title = ''
content = []
for line in lines:
    line = line.strip()

    # if line.startswith('［') and line.endswith('］'):
    if line.startswith('《') and line.endswith('》'):
    # if title_reg.match(line):
        if title:
            print(title)
            if prefix:
                title = prefix+'：'+title
            with open(title+'.pt', 'w')as to_w:
                to_w.writelines(
                    'title:'+title+'\r\ndate:'+date + '\r\n'+'\r\n'.join(content))

        title = line[1:-1]
        # title = title_reg.findall(line)[0]
        # title = str(int(title_reg.findall(line)[0]))
        
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
