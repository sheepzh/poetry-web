import re


def write(title, content, prefix=None, date=None):
    print(title)
    if not date:
        date = ''
    if prefix:
        title = prefix+'：'+title
    with open(title+'.pt', 'w')as to_w:
        to_w.writelines(
            'title:'+title+'\r\ndate:'+date + '\r\n'+'\r\n'.join(content))


def split_by_regrex(file_name, regrex_str, prefix='', date=None):
    title = ''
    content = []
    regrex = re.compile(regrex_str)

    with open(file_name + '.pt', 'r') as file:
        lines = file.readlines()[3:]

    for line in lines:
        line = line.strip()

        if regrex.match(line):
            if title:
                write(title, content, prefix=prefix, date=date)
            title = regrex.findall(line)[0]
            content = []
        else:
            content.append(line)
    if title:
        write(title, content, prefix, date)


def split_by_titles(file_name, titles=[], prefix='', date=None):
    l = len(titles)
    t = titles[0]
    content = []
    ti = 1
    tn = titles[ti]

    with open(file_name + '.pt', 'r') as file:
        lines = file.readlines()[3:]
    for line in lines:
        line = line.strip()
        if line == tn:
            if t:
                write(t, content, prefix, date)
            content = []
            t = tn
            ti += 1
            if l > ti:
                tn = titles[ti]
        else:
            content.append(line)

    if t:
        write(t, content, prefix, date)


# split_by_titles('哲学家和诗人（三首）', ['“有人吗？”', '致敬', '哲学家和诗人'], prefix='', date='')

split_by_regrex('灵魂深处的画卷（组诗）', r'^◆\s?(.*)$', prefix='灵魂深处的画卷', date='200612')
