#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-05-29 11:20:27
# @Author  : foodish
# @Email   : xbj1900@gmail.com
# @Link    : https://foodish.github.io


# 判断一个unicode是否是汉字
def is_chinese(uchar):
    if u'\u4e00' <= uchar <= u'\u9fff':
        return True
    else:
        return False
    # regex=re.compile("(?x) (?: [\w-]+ | [\x80-\xff]{3} )")  #中英文字符


# 判断一个unicode是否是数字
def is_number(uchar):
    if '\u0030' <= uchar <= '\u0039':
        return True
    else:
        return False


# 判断一个unicode是否是英文字母
def is_alphabet(uchar):
    if ('\u0041' <= uchar <= '\u005a') or ('\u0061' <= uchar <= '\u007a'):
        return True
    else:
        return False


# 判断是否非汉字，数字和英文字符
def is_other(uchar):
    if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):
        return True
    else:
        return False


if __name__ == "__main__":
    text = """
    ---
    作者：卜卜
    标签：日记
    哈哈哈哈
    或或或或
    """

    ch_count = 0
    for i in text:
        if (is_chinese):
            ch_count += 1
            print(i, ch_count)
