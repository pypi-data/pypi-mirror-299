import sys

from cmd import Cmd
from 西游记.西行 import 八十一难
from 西游记.语言 import 分析器, 分词器

class 交互(Cmd):
    prompt = '请问: '

    def default(self, 行):
        if 行 == "出发":
            游记 = 八十一难()
            游记.cmdloop()
        else:
            print("有" + str(分析器.按语法分词(分词器.分词(行))) + "个！")
        self.do_quit(行)

    def do_quit(self, arg):
        sys.exit()