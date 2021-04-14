# -*-coding:utf-8-*-
from flask import Flask, jsonify, g, send_file, request, render_template
import os
from functools import reduce
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False


def wrap_page(list_, page_num, page_size, need_total=True):
    total = len(list_)
    start_index = (page_num - 1) * page_size
    end_index = start_index + page_size

    if need_total:
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

    for root, _, fs in os.walk('data'):
        poet_cache = {}
        for f in fs:
            file = open(os.path.join(root, f), 'rb')
            poet = json.load(file)
            # 中文文件名编码懒得调了
            poet_cache[poet['n']] = poet
        g.poet_cache = poet_cache
        return poet_cache


@app.route("/")
def index():
    total = 0
    if 'poem_total' in g:
        total = g.get('poem_total')
    else:
        all_poets = list_all_poets()
        total = 0
        for poet_name in all_poets:
            poet = all_poets[poet_name]
            total += len(poet['w'])
        g.poem_total = total
    return render_template("index.html", total=total)
    # return send_file('templates/index.html')


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
    result = []
    for (k, v) in all_poets.items():
        if not word or word in k:
            result.append(
                {'name': v['n'], 'pinyin': v['p'], 'count': len(v['w'])})
    result = sorted(result, key=lambda p:  p['count'],  reverse=True)
    return jsonify(wrap_page(result, page_num, page_size))


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

    index = 0
    start_index = (page_num - 1) * page_size
    end_index = start_index + page_size

    list_ = []

    poet_list = []

    if poet_name:
        poet = all_poets.get(poet_name)
        if poet:
            poet_list.append(poet)
    else:
        poet_list = list(all_poets.values())
    for poet in poet_list:
        for poem in poet['w']:
            title = poem['t']
            if title_wd and title_wd not in title:
                continue
            contents = poem['l']
            date = poem['d']
            if content_wd:
                wd_appered = False
                for line in contents:
                    if content_wd in line:
                        wd_appered = True
                        break
                if not wd_appered:
                    continue
            if index >= start_index and index < end_index:
                pp = {
                    'title': title, 'poet': poet['n'], 'date': date, 'contents': contents}
                list_.append(pp)
            index += 1
            if index >= end_index:
                return jsonify(wrap_page(list_, page_num, page_size, need_total=False))
    return jsonify(wrap_page(list_, page_num, page_size, need_total=False))


@app.route('/poet/<poet_name>/poems')
def poems_by_poet(poet_name):
    all_poets = list_all_poets()
    if poet_name not in all_poets:
        print(poet_name, 'not found')
        poems = []
    else:
        poems = all_poets[poet_name]['w']
    # 内容
    content_wd = request.args.get('wd')
    page_num, page_size = get_page_args()

    list_ = []
    max_line = 3
    for poem in poems:
        title = poem['t']
        date = poem['d']
        contents = poem['l']
        pp = {'title': title, 'date': date}
        lines = {}
        if content_wd:
            line_index = 0
            for i in range(0, len(contents)):
                if line_index == max_line:
                    break
                line = contents[i]
                if content_wd in line:
                    lines[str(i)] = line
                    line_index += 1
        else:
            for i in range(0, min(max_line, len(contents))):
                lines[str(i)] = contents[i]
        if len(lines.keys()):
            pp['lines'] = lines
            list_.append(pp)
    return jsonify(wrap_page(list_, page_num, page_size))


@app.route('/poet/<poet_name>/list')
def poems_list(poet_name):
    all_poets = list_all_poets()
    if poet_name not in all_poets:
        print(poet_name, 'not found')
        return '404'

    poems = all_poets[poet_name]['w']
    poem_titles = list(map(lambda poem: poem['t'], poems))
    poem_titles = sorted(poem_titles)
    return render_template('list.html', list=poem_titles, poet=poet_name)


@app.route('/poet/<poet_name>/poem/<poem_name>')
def read_poem(poet_name, poem_name):
    all_poets = list_all_poets()
    if poet_name not in all_poets:
        return '404'

    poems = all_poets[poet_name]['w']
    target_poem = None
    for poem in poems:
        if poem_name == poem['t']:
            target_poem = poem
            break
    if not target_poem:
        return '404'

    return render_template('poem.html', poem=target_poem, poet=poet_name)

