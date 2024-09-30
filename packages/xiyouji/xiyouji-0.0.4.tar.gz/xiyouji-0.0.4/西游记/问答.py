import re
import sys

from cmd import Cmd

class 数字母(Cmd):
    prompt = '请问: '

    def default(self, 行):
        问题 = 行
        分析 = re.search(r"“(\w+)”.+“(\w)”", 问题)
        词 = 分析.group(1)
        字母 = 分析.group(2)
        print("有" + str(词.count(字母)) + "个！")
        self.do_quit(行)

    def do_quit(self, arg):
        sys.exit()