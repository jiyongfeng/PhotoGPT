#!/usr/bin/env python
# coding=utf-8

"""
 * @Author       : JIYONGFENG jiyongfeng@163.com
 * @Date         : 2024-05-22 21:24:43
 * @LastEditors  : JIYONGFENG jiyongfeng@163.com
 * @LastEditTime : 2024-05-22 21:42:56
 * @Description  :
 * @Copyright (c) 2024 by ZEZEDATA Technology CO, LTD, All Rights Reserved.
"""
import re


def extract_dateComponents(match):
    """
    Extracts the year, month, and day from a regex match.
    """
    year = "20" + match.group(1)
    month = match.group(2)
    day = match.group(3)
    return f"{year}-{month}-{day}", year, month, day


def get_photo_date(filename):
    """
    Extracts the date from the file name.
    """
    # 合并两个正则表达式到一个
    pattern = r"20(\d{2})(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])|20(\d{2})-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])"

    match = re.search(pattern, filename)
    if match:
        # 成功匹配时，调用extract_dateComponents处理匹配结果
        date_str, year, month, day = extract_dateComponents(match)
        # 可以在这里进一步处理或验证日期，例如检查月份和日期的合法性
        return date_str
    else:
        # 未匹配时，返回None或其他自定义消息
        return None


file_name = "20231205_09-01-02.jpg"
print(get_photo_date(file_name))
