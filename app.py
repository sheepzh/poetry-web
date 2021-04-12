from flask import Flask, jsonify, g, send_file, request
import os
from functools import reduce
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False


def wrap_page(list_, page_num, page_size, need_total=True):
    total = len(list_)
    start_index = (page_num - 1) * page_size
    end_index = start_index + page_size
    if end_index > total:
        end_index = total
    if total < start_index:
        list_ = []
    else:
        list_ = list_[start_index:end_index]
    page = {'list': list_, 'page': page_num, 'size': page_size}

    if need_total:
        page['total'] = total

    return page


@app.route("/")
def index():
    return send_file("index.html")


def get_poet_name_from_dir_name(d):
    """
        get poet info from the directory name

        "张枣_zhangzao"  => ("张枣", "zhangzao")
        "a_b_c_abc"  =>  ("a_b_c", "abc")
        "abc"  =>  (None, None)
    """
    try:
        split_index = d.rindex('_')
        return (d[:split_index], d[split_index+1:])
    except ValueError:
        print(d)
        return (None, None)


def list_all_poets():
    if 'poets_cache' in g:
        return g.get('poet_cache')

    for root, ds, _ in os.walk('data'):
        poet_cache = []
        for d in ds:

            poet = {}
            name, py = get_poet_name_from_dir_name(d)
            poet['name'] = name
            poet['py'] = py
            poet_dir = os.path.join(root, d)

            for _, _, poem_fs in os.walk(poet_dir):
                poet['count'] = len(poem_fs)

            poet_cache.append(poet)
        poet_cache = sorted(
            poet_cache, key=lambda poet: poet['count'], reverse=True)
        g.poet_cache = poet_cache
        return poet_cache


def get_page_args():
    page_num = request.args.get('pn')
    if not page_num or int(page_num) < 0:
        page_num = 1
    page_size = request.args.get('ps')
    if not page_size or int(page_size) < 0 or int(page_size) > 50:
        page_size = 10
    return (int(page_num), int(page_size))


@app.route("/poets")
def poets():
    """
      GET /poets?wd=[关键字?]&pn=[页数?]&ps=[页大小]

      {
        list:[
          {
            'name': '张枣',
            'py': 'zhangzao'
          },
          ...
        ],
        total: 200,
        page: 1,
        size: 10
      }
    """
    all_poets = list_all_poets()
    word = request.args.get('wd')
    page_num, page_size = get_page_args()
    if word:
        all_poets = list(filter(lambda p: word in p['name'], all_poets))
    return jsonify(wrap_page(all_poets, page_num, page_size))


@app.route('/poems')
def poems():
    # 精确查询
    poet_name = request.args.get('poet')
    # 模糊查询
    title_wd = request.args.get('title')
    # 内容
    content_wd = request.args.get('wd')

    page_num, page_size = get_page_args()

    all_poets = list_all_poets()
    if poet_name:
        all_poets = list(filter(lambda poet: poet_name in poet['name']))

    index = 0
    start_index = (page_num - 1) * page_size
    end_index = start_index + page_size

    list_ = []

    for poet in all_poets:
        poet_dir = os.path.join('data', poet['name'] + '_' + poet['py'])
        for root, _, fs in os.walk(poet_dir):
            for f in fs:
                title = f[:-3]
                if title_wd and title_wd not in title:
                    continue
                with open(os.path.join(root, f), 'r') as file:
                    lines = file.readlines()
                    lines = list(map(lambda line: line.strip(), lines))
                    if not len(lines):
                        print('empty lines: ', f)
                    date_line = lines[1]
                    if len(date_line) > 5:
                        date = date_line[5:]
                    else:
                        date = ''
                    contents = lines[3:]
                    if content_wd:
                        wd_appered = False
                        for line in contents:
                            if content_wd in line:
                                wd_appered = True
                                break
                        if not wd_appered:
                            continue
                    if index >= start_index and index < end_index:
                        poem = {
                            'title': title, 'poet': poet['name'], 'date': date, 'contents': contents}
                        list_.append(poem)
                    index += 1
                    if index >= end_index:
                        return jsonify(wrap_page(list_, page_num, page_size, need_total=False))
    return jsonify(wrap_page(list_, page_num, page_size, need_total=False))
