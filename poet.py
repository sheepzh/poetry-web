
from poem import Poem


class Poet:
    def __init__(self, name, pinyin):
        self.n = name
        self.p = pinyin
        # works
        self.w = []

    def append_poem(self, poem: Poem):
        self.w.append(poem)
