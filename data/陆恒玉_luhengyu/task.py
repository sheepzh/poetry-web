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


# split_by_titles('打开花朵或者时光诉说（组诗）（下）', ['2月24日的雨', '露水', '雾失楼台','君子兰','怀念','马渡桥','春天的麦地','搬出我们的犁铧','风','之上','还有什么','明天','黑夜的深度','记录，3月2日的早晨','在春天里打下暖暖江山','鸟声在键盘上跳跃','骑着群山奔跑'], prefix='', date='')

def index_to_title(_title, index): return str(index)


def two_regrex(arr): return arr[0].strip() + '——' + arr[1].strip()


split_by_regrex('阳光逼出骨头里的寒气（续）', r'^《(.*)》$', prefix='', date='2008')
# split_by_regrex('小淡词（连载・八）', r'^《小淡词 (\d{1,3})》(.*)$', date='201211', prefix='小淡词', regrex_map=two_regrex)
