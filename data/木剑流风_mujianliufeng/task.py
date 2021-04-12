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


def split_by_regrex(file_name, regrex_str, prefix='', date=None, title_map=None, regrex_map=None):
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
            if regrex_map:
                title = regrex_map(regrex.findall(line)[0])
            else:
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


# split_by_titles('开平印象（组诗）', ['城市广场', '赤坎古镇', '开平碉楼', '时间', '森林', '镜子', '那一道墙', '离'], prefix='', date='')


def index_to_title(_title, index): return str(index)


def two_regrex(arr): return arr[0].strip() + '——' + arr[1].strip()


split_by_regrex('一墙之隔（组诗）', r'^《(.*)》$', prefix='', date='20091010')
# split_by_regrex('小淡词（连载・八）', r'^《小淡词 (\d{1,3})》(.*)$', date='201211', prefix='小淡词', regrex_map=two_regrex)
