import re


def write(title, content, prefix=None, date=None):
    print(title)
    if not date:
        date = ''
    if prefix:
        title = prefix + '：' + title
    with open(title + '.pt', 'w')as to_w:
        to_w.writelines(
            'title:' + title + '\r\ndate:' + date + '\r\n' + '\r\n'.join(content))


def split_by_regrex(file_name, regrex_str, prefix='', date=None, title_map=None):
    title = ''
    content = []
    regrex = re.compile(regrex_str)
    index = 1
    with open(file_name + '.pt', 'r') as file:
        lines = file.readlines()[3:]

    for line in lines:
        line = line.strip()

        if regrex.match(line):
            if title:
                if title_map:
                    title = title_map(title, index)
                write(title, content, prefix=prefix, date=date)
                index += 1
            title = regrex.findall(line)[0]
            content = []
        else:
            content.append(line)
    if title:
        if title_map:
            title = title_map(title, index)
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


# split_by_titles('爆炸的肉体及其他（组诗）', ['透视', '紫罗兰', '黄昏，或者光明','爆炸的肉体'], prefix='', date='')

def index_to_title(_title, index): return str(index)


# split_by_regrex('短诗一组', r'^\d{2}$', prefix='短诗', date='2009', title_map=index_to_title)

split_by_regrex('七月悲歌（四首）', r'^(\d)、$', prefix='七月悲歌', date='200903')
