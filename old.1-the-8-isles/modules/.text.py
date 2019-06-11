# -*- coding: utf-8 -*-
import os, re

with open("lines.txt", "a", encoding="utf-8") as lines:
    for module in os.listdir():
        if module == ".text.py" or module == "lines.txt" or module == "xwu_nud35.py":
            continue
        with open(module, "r") as file:
            print(module)
            for line in file.read().replace("'''", "").split("\n"):
                for quote in re.findall("'.+'", line):
                    print(quote)
                    lines.write(quote + "\n")
