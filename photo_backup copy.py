#!/usr/bin/env python
# coding=utf-8

"""
 * @Author       : JIYONGFENG jiyongfeng@163.com
 * @Date         : 2024-05-21 11:33:40
 * @LastEditors  : JIYONGFENG jiyongfeng@163.com
 * @LastEditTime : 2024-05-31 09:35:58
 * @Description  :
 * @Copyright (c) 2024 by ZEZEDATA Technology CO, LTD, All Rights Reserved.
"""

import re
import os
import sys
import shutil
import hashlib
from PIL import Image
from PIL.ExifTags import TAGS


# 定义支持的图片文件类型
SUPPORTED_IMAGE_TYPES = ('.jpg', '.jpeg', '.png', '.JPG', '.bmp', '.gif')
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


def get_photo_date(file_path):
    '''Get the date when the photo was taken.'''
    # Open the file using the file path
    with open(file_path, 'rb') as f:
        # Read the file content
        content = f.read()
        # Find the date in the file content
        date_str = re.search(rb'\d{4}:\d{2}:\d{2} \d{2}:\d{2}:\d{2}', content)
        # If a date is found, return it
        if date_str:
            return date_str.group().decode('utf-8')
        else:
            return None
    try:
        with Image.open(file_path) as img:
            exif_data = img._getexif()
            # 判断是否有exif信息，并且日期信息不为空
            if 'EXIF DateTimeOriginal' in exif_data:
                date_str = exif_data['EXIF DateTimeOriginal']
                return date_str
            # 否则执行get_photo_date_from_filename函数
            else:
                return get_photo_date_from_filename(file_path)

            if exif_data is not None:
                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)
                    if tag_name == DATE_TIME_ORIGINAL_TAG:
                        date = value.split(' ')[0].replace(':', '-')
                        return date
            else:
                return '0000-00-00'
    except (OSError, IsADirectoryError, KeyError, TypeError) as e:
        print(f"Error processing {file_path}: {e}")


def copy_photos_by_date(source_dir, destination_dir):
    '''
    This function copies all the photos in the source directory to the destination directory, grouped by date.
    '''
    file_count = 0
    validate_folder_path(source_dir)
    validate_folder_path(destination_dir)
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            # 判断文件是否是图片文件
            if file.endswith(SUPPORTED_IMAGE_TYPES):

                file_path = os.path.join(root, file)
                try:
                    date = get_photo_date(file_path)
                    print(f"{file_path} : {date}")
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
                            # 计算md5
                            source_md5 = get_md5(file_path)
                            destination_md5 = get_md5(destination_file_path)
                            if source_md5 == destination_md5:
                                print('{} is already exist'.format(file))
                                break
                            else:
                                # 将文件重命名
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
        print("Usage: python photo_backup.py <image_source_path> <image_destination_path>")
        sys.exit(1)

    source_folder = sys.argv[1]
    destination_folder = sys.argv[2]
    if validate_folder_path(source_folder):
        sys.exit(1)
    if validate_folder_path(destination_folder):
        sys.exit(1)

    copy_photos_by_date(source_folder, destination_folder)


if __name__ == "__main__":
    main()
