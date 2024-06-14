#!/usr/bin/env python
# coding=utf-8

"""
 * @Author       : JIYONGFENG jiyongfeng@163.com
 * @Date         : 2024-05-21 16:19:02
 * @LastEditors  : JIYONGFENG jiyongfeng@163.com
 * @LastEditTime : 2024-05-23 10:56:47
 * @Description  :
 * @Copyright (c) 2024 by ZEZEDATA Technology CO, LTD, All Rights Reserved.
"""
import re
import os
from PIL import Image
from PIL.ExifTags import TAGS


def extract_dateComponents(match):
    """
    Extracts the year, month, and day from a regex match.
    """
    print("match:", match.group(1))
    year = "20" + match.group(1)
    print("match:", match.group(2))
    month = match.group(2)
    print("match:", match.group(3))
    day = match.group(3)
    return f"{year}-{month}-{day}", year, month, day


def get_photo_date_from_filename(filename):
    """
    Extracts the date from the file name.
    """
    # 合并两个正则表达式到一个
    pattern1 = r"20(\d{2})(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])"
    pattern2 = r"20(\d{2})-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])"
    match1 = re.search(pattern1, filename)
    match2 = re.search(pattern2, filename)

    if match1:
        # 成功匹配时，调用extract_dateComponents处理匹配结果
        date_str, year, month, day = extract_dateComponents(match1)
        # 可以在这里进一步处理或验证日期，例如检查月份和日期的合法性
        return date_str
    elif match2:
        date_str, year, month, day = extract_dateComponents(match2)
        # 可以在这里进一步处理或验证日期，例如检查月份和日期的合法性
        return date_str

    else:
        # 未匹配时，返回None或其他自定义消息
        return None


def get_photo_date(file_path):
    """ Read photo exif date and return photo date, formatted as YYYY-MM-DD

    Args:
        file_path (str): file path

    Returns:
        str: date formatted as YYYY-MM-DD
    """

    file_name = os.path.basename(file_path)
    parent_dir = os.path.basename(os.path.dirname(file_path))
    date_fromfilename = get_photo_date_from_filename(file_name)
    date_fromparent = get_photo_date_from_filename(parent_dir)
    print(f"{file_path} : {date_fromfilename}")
    print(f"{file_path} : {date_fromparent} ")
    try:
        with Image.open(file_path) as img:
            exif_data = img._getexif()
            # check if the exif data is not None
            if exif_data is not None:
                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)
                    # check if the tag DateTimeOriginal exists
                    if tag_name == 'DateTimeOriginal':
                        # extract the date and time from the value
                        # check if the value is like 2011:11:22
                        if re.match(r"20\d{2}:\d{2}:\d{2}", value):
                            date = value.split(' ')[0].replace(':', '-')
                            return date
    except (OSError, IsADirectoryError, KeyError, TypeError) as e:
        print(f"Error processing {file_path}: {e}")

    if date_fromfilename:
        return date_fromfilename
    elif date_fromparent:
        return date_fromparent
    else:
        return "2000-01-01"


filestr = '/Users/jiyongfeng/SynologyDrive/99_test/Python/app/PhotoGPT/source/2003/01/2014-11-22/IMG_4749.JPG'
string = '2014-11-31.JPG'
print(get_photo_date_from_filename(string))
# print(get_photo_date(filestr))
