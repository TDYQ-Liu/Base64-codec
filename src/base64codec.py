"""
MIT License

Copyright (c) 2021 TDYQ-Liu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import base64
import glob
import sys
import os.path
import argparse

class Base64_codec:

    def __init__(self, data: list):
        self.__data = data

    def encode_64(self) -> list:
        pre_data = []
        ret_data = []
        for row in self.__data:
            pre_data.append(base64.b64encode(row.encode()))
        for row in pre_data:
            ret_data.append(row.decode('utf-8') + '\n')
        return ret_data

    def decode_64(self) -> list:
        pre_data = []
        ret_data = []
        for row in self.__data:
            try:
                pre_data.append(base64.b64decode(row.encode()))
            except:
                pre_data.append(row)
        for row in pre_data:
            try:
                ret_data.append(row.decode('utf-8'))
            except:
                if isinstance(row, bytes):
                    ret_data.append(str(row) + "\n")
                else:
                    ret_data.append(row)
        return ret_data

def get_filelist(pathname) -> list:
    return glob.glob(pathname)

def get_data(file) -> list:
    with open(file, 'r', newline="", encoding='utf-8') as f:
        ls = f.readlines()
    return ls

def process_filename(file) -> tuple:
    file_basename = os.path.basename(file)
    file_root = os.path.splitext(file_basename)[0]
    file_ext = os.path.splitext(file_basename)[1]
    return file_basename, file_root, file_ext

def output_file(file, data) -> None:
    with open(file, 'w', newline="", encoding='utf-8') as f:
        f.writelines(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="BASE64 CODEC")
    parser.add_argument("-c", "--codec", 
                        type=str, 
                        default="encode", 
                        help="check encode or decode")
    parser.add_argument("-p", "--path", 
                        type=str, 
                        default=os.path.join(sys.path[0], "*.txt"), 
                        help="the file path")
    parser.add_argument("-d", "--destination", 
                        type=str, 
                        default=sys.path[0], 
                        help="the output file destination")
    args = parser.parse_args()

    file_list = get_filelist(args.path)
    for file in file_list:
        f_data = get_data(file)
        f_name = process_filename(file)

        if args.codec == "encode":
            value_data = Base64_codec(f_data).encode_64()
            if os.path.splitext(args.destination)[1] == "":
                file_name = os.path.join(args.destination, f_name[1] + "_encode" + f_name[2])
            else:
                file_name = args.destination
        elif args.codec == "decode":
            value_data = Base64_codec(f_data).decode_64()
            if os.path.splitext(args.destination)[1] == "":
                file_name = os.path.join(args.destination, f_name[1] + "_decode" + f_name[2])
            else:
                file_name = args.destination
        else:
            print("the option error")

        output_file(file_name, value_data)
        print("{} successfull!  file: {} ".format(args.codec, f_name[0]))
