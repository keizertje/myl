from keyword import kwlist
import builtins
from tkinter import Text
from typing import Callable, Any


class Color:
    indextype = list[int | tuple[int, int]]
    isending: Callable[[Any, str, int, int], bool] = lambda self, string, start, end: not (((string[start - 1].isidentifier()) if (start != 0) else False) or
                                                                                           ((string[end].isidentifier()) if (end != len(string)) else False))
    findWords: Callable[[Any, str, str], indextype] = lambda self, s, w: [(i, i + len(w)) for i, v in enumerate(s) if s[i:i + len(w)] == w and self.isending(s, i, i + len(w))]
    to_index: Callable[[Any, int], str] = lambda self, i: f"1.0+{i}c"

    def __init__(self, text: Text) -> None:
        self.text: Text = text
        self.inp: str = self.text.get("1.0", "end-1c")

        self.ignore: Color.indextype = []
        self.strings: Color.indextype = []
        self.comments: Color.indextype = []
        self.numbers: Color.indextype = []
        self.builtins: Color.indextype = []
        self.keywords: Color.indextype = []
        self.names: Color.indextype = []
        self.todo: Color.indextype = []
        self.errors: Color.indextype = []

        self.types: dict[str] = {"strings": {"foreground": "#db0"}, "comments": {"foreground": "#a87", "font": "arial 11 italic"}, "numbers": {"foreground": "#f40"}, "builtins": {"foreground": "#e81"}, "keywords": {"foreground": "#f93"}, "errors": {"background": "#fcc", "foreground": "#f00"}, "todo": {"foreground": "#ee0"}, "names": {"foreground": "#750"}}
        self.types_list: list[str] = list(self.types.keys())

        self.in_double_string: bool = False
        self.in_single_string: bool = False
        self.in_comment: bool = False
        self.dont_check: bool = False

        self.str_int_comment()
        self.builtins_keywords()
        self.add_tags()

        for i in self.types_list:
            self.text.tag_config(i, **self.types[i])

    def add_tag(self, name: str, start: int, end: int):
        self.text.tag_add(name, self.to_index(start), self.to_index(end))

    def add_tags(self):
        for i in self.text.tag_names():
            self.text.tag_delete(i)
        for i in self.types_list:
            items = self.__getattribute__(i)
            for j in items:
                if type(j) == int:
                    self.add_tag(i, j, j + 1)
                elif type(j) == tuple:
                    self.add_tag(i, j[0], j[1])

    def str_int_comment(self):
        for i, v in enumerate(self.inp):
            if v == '"' and not self.in_comment and not self.in_single_string:
                self.in_double_string = not self.in_double_string
                if not self.in_double_string:
                    self.strings.append(i)
            elif v == "'" and not self.in_comment and not self.in_double_string:
                self.in_single_string = not self.in_single_string
                if not self.in_single_string:
                    self.strings.append(i)
            elif v == "#" and not self.in_double_string and not self.in_single_string:
                self.in_comment = True
            elif self.in_comment and v == "\n":
                self.in_comment = False

            if self.in_comment or self.in_single_string or self.in_double_string:
                self.ignore.append(i)

            if self.in_comment:
                self.comments.append(i)
            elif self.in_double_string or self.in_single_string:
                self.strings.append(i)
                if i == len(self.inp) - 1:
                    self.errors.append(i)
            elif v in [str(j) for j in range(10)]:
                self.numbers.append(i)

    def builtins_keywords(self):
        builtin_f = dir(builtins)
        keywords = list(kwlist)
        for i in builtin_f:
            usages = self.findWords(self.inp, i)
            for j in usages:
                if j[0] not in self.ignore:
                    self.builtins.append(j)
        for k in keywords:
            usages = self.findWords(self.inp, k)
            for l in usages:
                if l[0] not in self.ignore:
                    self.keywords.append(l)
                    if k == "def" or k == "class":
                        line = self.text.get(self.to_index(l[0]), self.to_index(l[0]) + " lineend")
                        bracket = line.find("("); double_point = line.find(":")
                        veel = len(line)
                        end = l[0] + min(bracket if bracket != -1 else veel, double_point if double_point != -1 else veel)
                        self.names.append((l[1], end))
