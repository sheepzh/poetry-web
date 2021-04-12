import sys
import os
import pickle
from poem import Poem
from poet import Poet

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
        return Poem(title, date, lines)


def parse_poet(dir_name, root):
    try:
        split = dir_name.rindex('_')
        poet = Poet(dir_name[:split], dir_name[split+1:])
        for root, _, fs in os.walk(os.path.join(root, dir_name)):
            for f in fs:
                if f.endswith('.pt'):
                    poem = parse_poem(os.path.join(root, f))
                    poet.append_poem(poem)
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
            with open(os.path.join('data', poet.n), 'wb') as file:
                pickle.dump(poet, file)
