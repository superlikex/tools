# -*- coding: utf-8 -*-
import os
import sys
import re
import subprocess

def check_argv():
    if len(sys.argv) != 4:
        print("usage: %s < path of log file > < path of addr2line > < path of elf >" % sys.argv[0])
        sys.exit()
    else:
        print("Check files if exist：")
        for i in range(1, 4):
            file_name = sys.argv[i]
            if os.path.exists(file_name):
                print("\033[32m     " + sys.argv[i] + " exist\033[0m")
            else:
                print("\033[31m     Can not find " + sys.argv[i] + "\033[0m")
                sys.exit()

def main():
    check_argv()

    log_path = sys.argv[1]
    addr2line_path = sys.argv[2]
    elf_path = sys.argv[3]

    result_path = log_path + "_result_file"
    print("start... results will be saved in \033[33m%s\033[0m" % result_path)
    print("waiting...")
    with open(log_path, 'r', errors='ignore') as f1:
        lines = f1.readlines()
        with open(result_path, 'w') as f2:
            dict = {}
            for i in range(len(lines)):
                res = re.findall(r"backtrace: (0x[0-9a-f]{8})", lines[i])
                if res:
                    if res[0] in dict:
                        f2.write(dict.get(res[0]))
                    else:
                        cmd = addr2line_path + " -e " + elf_path + " " + res[0] + " -f -a -p -C"
                        result = subprocess.check_output(cmd, shell=True).decode('utf-8')
                        dict[res[0]] = result
                        f2.write(result)
                else:
                    if lines[i].strip() != "":
                        f2.write(lines[i])
    print("done!")

if __name__ == "__main__":
    main()
