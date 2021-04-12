import sys
import os
import json

if len(sys.argv) < 2:
    print('no origin data')
    quit()

origin_dir = sys.argv[1]


def parse_poem(poem_path):
    with open(poem_path, 'r')as file:
        lines = list(map(lambda s: s.strip(), file.readlines()))
        title = lines[0][6:]
        date = lines[1][5:]
        lines = lines[3:]
        return {'t': title, 'd': date, 'l': lines}


def parse_poet(dir_name, root):
    try:
        split = dir_name.rindex('_')
        poet = {'n': dir_name[:split], 'p': dir_name[split+1:]}
        works = []
        for root, _, fs in os.walk(os.path.join(root, dir_name)):
            for f in fs:
                if f.endswith('.pt'):
                    poem = parse_poem(os.path.join(root, f))
                    works.append(poem)
        poet['w'] = works
        return poet
    except IOError:
        return None


if not os.path.exists('data'):
    os.makedirs('data')

poets = []

for root, ds, _ in os.walk(origin_dir):
    for d in ds:
        poet = parse_poet(d, root)
        if poet:
            with open(os.path.join('data', poet['n']), 'w') as file:
                file.writelines(json.dumps(poet, ensure_ascii=False))
