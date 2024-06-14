#!/usr/bin/env python
# coding=utf-8

"""
 * @Author       : JIYONGFENG jiyongfeng@163.com
 * @Date         : 2024-05-21 11:33:40
 * @LastEditors  : JIYONGFENG jiyongfeng@163.com
 * @LastEditTime : 2024-05-23 15:28:52
 * @Description  :
 * @Copyright (c) 2024 by ZEZEDATA Technology CO, LTD, All Rights Reserved.
"""

import os
import re
import sys
import shutil
import hashlib
from PIL import Image
from PIL.ExifTags import TAGS


# 定义支持的图片文件类型
SUPPORTED_IMAGE_TYPES = ('.jpg', '.jpeg', '.png', 'JPG')
# 定义需要从Exif数据中提取的标签名称
DATE_TIME_ORIGINAL_TAG = 'DateTimeOriginal'
MAKE_TAG = 'Make'


def validate_folder_path(folder_path):
    """
    check if the folder path is valid
    """
    if not os.path.isdir(folder_path):
        raise ValueError(f"{folder_path} is not a valid directory.")


def generate_unique_filename(destination_path, base_name):
    """generate a unique filename"""
    unique_name = f"{base_name}"
    unique_path = os.path.join(destination_path, unique_name)
    if os.path.exists(unique_path):
        counter = 1
        while True:
            unique_name = f"{base_name.split('.')[-2]}({counter}).{base_name.split('.')[-1]}"
            unique_path = os.path.join(destination_path, unique_name)
            if not os.path.exists(unique_path):
                return unique_name
            counter += 1
    else:
        return unique_name


def get_md5(file_path):
    """计算文件的MD5哈希值"""
    with open(file_path, 'rb') as file:
        md5_hash = hashlib.md5()
        for chunk in iter(lambda: file.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()


def extract_dateComponents(match):
    """
    Extracts the year, month, and day from a regex match.
    """
    year = "20" + match.group(1)
    month = match.group(2)
    day = match.group(3)
    return f"{year}-{month}-{day}", year, month, day


def get_photo_date_from_filename(filename):
    """
    Extracts the date from the file name.
    """
    # match date format like 20221111
    pattern1 = r"20(\d{2})(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])"
    # match date format like 2022-11-11
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

    return get_photo_date_from_filename(file_name)


def copy_photos_by_date(source_dir, destination_dir, supported_image_types=SUPPORTED_IMAGE_TYPES):
    """ copy photos by date

    Args:
        source_dir (_type_): _description_
        destination_dir (_type_): _description_
    """
    file_count = 0
    validate_folder_path(source_dir)
    validate_folder_path(destination_dir)
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            # check if the file is an image
            if file.endswith(supported_image_types):

                file_path = os.path.join(root, file)
                parent_dir = os.path.basename(
                    os.path.dirname(file_path))
                try:
                    # get the date of the photo, default to 0000-00-00
                    date_fromfile = get_photo_date(file_path)
                    date_fromparent = get_photo_date_from_filename(parent_dir)
                    if date_fromfile:
                        date = date_fromfile
                        print(f"{file_path} : date has got from file {date}")
                    elif date_fromparent:
                        date = date_fromparent
                        print(f"{file_path} : date has got from dir {date}")
                    else:
                        date = "2000-01-01"
                        print(f"{file_path} : date has set to default {date}")
                    # create destination directory if it doesn't exist

                    year = date.split('-')[0]
                    month = date.split('-')[1]
                    day = date.split('-')[2]
                    date = f"{year}/{month}/{date}"
                    destination_dir_path = os.path.join(
                        destination_dir, date)
                    destination_file_path = os.path.join(
                        destination_dir_path, file)
                    if os.path.exists(destination_dir_path):
                        if os.path.exists(destination_file_path):
                            # md5
                            source_md5 = get_md5(file_path)
                            destination_md5 = get_md5(destination_file_path)
                            if source_md5 == destination_md5:
                                print(f'{file} is already exist')
                                break
                            else:
                                # rename file
                                rename_path = generate_unique_filename(
                                    destination_dir_path, file)
                                # copy file
                                shutil.copy2(file_path, rename_path)
                        else:

                            shutil.copy(file_path, destination_file_path)
                    else:
                        os.makedirs(destination_dir_path)
                        shutil.copy(file_path, destination_file_path)
                    file_count += 1
                except Exception as e:
                    print(e)
    print(f"{file_count} files copied")


def main():
    """main
    """
    if len(sys.argv) < 3:
        print("Usage: python photo_backup.py <image_source_path> <image_destination_path> <image_file_type_list>")
        sys.exit(1)

    source_folder = sys.argv[1]
    destination_folder = sys.argv[2]
    support_image_types = sys.argv[3]
    if validate_folder_path(source_folder):
        sys.exit(1)
    if validate_folder_path(destination_folder):
        sys.exit(1)

    copy_photos_by_date(source_folder, destination_folder, support_image_types)


if __name__ == "__main__":
    main()
