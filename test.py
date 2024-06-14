#!/usr/bin/env python
# coding=utf-8

"""
 * @Author       : JIYONGFENG jiyongfeng@163.com
 * @Date         : 2024-05-21 12:04:37
 * @LastEditors  : JIYONGFENG jiyongfeng@163.com
 * @LastEditTime : 2024-06-14 19:04:14
 * @Description  :
 * @Copyright (c) 2024 by ZEZEDATA Technology CO, LTD, All Rights Reserved.
"""
import os
import sys
from PIL import Image
from PIL import _ImageCrop
from PIL.ExifTags import TAGS


def print_exif_info(image_path):
    """print exif information

    Args:
        image_path (string): the path of the image file
    """
    try:
        with _ImageCrop.open(image_path) as img:
            exif_data = img._getexif()
            if exif_data is not None:
                for tag_id, value in exif_data.items():
                    tag_name = TAGS.get(tag_id, tag_id)
                    print(f"{tag_name}: {value}")
            else:
                print("No Exif data found.")
    except (AttributeError, FileNotFoundError, IsADirectoryError):
        print(f"Error opening '{image_path}'")


def main():
    """ main fucntion
    """

    if len(sys.argv) < 2:
        print("Usage: python test_exif.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    if not os.path.isfile(image_path):
        print(f"'{image_path}' is not a valid file.")
        sys.exit(1)

    print_exif_info(image_path)


if __name__ == "__main__":
    main()
