#!/usr/bin/python3

import argparse
import random
import getch
import time
import sys
import os

colors = [
    "\033[38;2;117;117;117m",
    "\033[38;2;97;97;97m",
    "\033[38;2;77;77;77m",
    "\033[38;2;57;57;57m",
    "\033[38;2;37;37;37m",
    "\033[38;2;17;17;17m",
    "\033[38;2;0;0;0m"
]

def get_chr():
    inpt = getch.getch()
    if inpt == '\x7f':
        return -1
    elif inpt in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-'#:":
        return inpt
    elif inpt in (' ', '\n'):
        return 1

    return ''

def build_nexts(nexts):
    final = '\033[0m'
    for i in range(7):
        if i >= len(nexts):
            break
        final += "\033[48;2;0;0;0m {}{}\033[0m".format(colors[i], nexts[i])
    return final

def cleared(string):
    l = ''
    is_in_esc_code = False
    for char in string:
        if char in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r" and not is_in_esc_code:
            l += char
        if char == "\033":
            is_in_esc_code = True
        if char == 'm':
            is_in_esc_code = False
    return l

def clear():
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")

def run_turn(target, nexts):
    a = 0
    string = ''
    fnexts = build_nexts(nexts)
    total = target + fnexts
    buffer = cleared(total)
    l = len(buffer)
    sys.stdout.write(f"\033[48;2;0;0;0m\033[94m{total}\r")
    sys.stdout.flush()
    inpt = None
    while inpt != 1:
        try:
            inpt = get_chr()
        except OverflowError:
            continue
        if inpt == -1:
            a += 1
            string = string[:-1]
            sys.stdout.write("\b\033[48;2;0;0;0m")
            current_word_i = (buffer[:len(string)]).count(' ')
            if current_word_i == 0:
                sys.stdout.write("\033[94m")
            elif len(string) >= len(buffer):
                sys.stdout.write("\033[0m \b")
                sys.stdout.flush()
                continue
            else:
                sys.stdout.write(colors[current_word_i - 1])
            sys.stdout.write(buffer[len(string)])
            sys.stdout.write("\b")
            sys.stdout.flush()
            continue
        if inpt in (0, 1):
            continue
        if type(inpt) != str:
            raise ValueError(f"Got an unexpected value {inpt} of type {type(inpt)}")

        string += inpt
        a += 1
        
        if not inpt:
            continue

        sys.stdout.write("\033[48;2;0;0;0m")
        sys.stdout.write("\033[92m" if target.startswith(string) else "\033[91m")
        sys.stdout.write(inpt)
        sys.stdout.flush()
    
    sys.stdout.write("\033[0m" + (' ' * l) + '\r')

    return (a, string)

def filepath(path):
    if os.path.isfile(path):
        return path
    else:
        raise FileNotFoundError(path)

def build_parser():
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description="Test your writing speed !",
    )
    parser.add_argument(
        "-d", "--database",
        help="The wordlist to use.",
        type=filepath,
        required=True
    )
    parser.add_argument(
        "-n", "--number",
        help="The amount of word to ask",
        type=int,
        default=30
    )
    parser.add_argument(
        "-p", "--penalty",
        help="The penalty value (the bigger it is, the more it will affect when missing a word. It will also affect more smaller words)",
        type=float,
        default=1.0
    )
    parser.add_argument
    return parser

if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    with open(args.database, 'r') as f:
        db = f.read().split('\n')
    liste = []
    for i in range(args.number):
        liste.append(random.choice(db))
    clear()
    stats = {}
    stats["wasked"] = args.number
    stats["casked"] = sum([len(word) for word in liste])
    stats["cpress"] = 0
    stats["correct"] = 0
    stats["penality"] = 0
    stats["totaltime"] = 0

    total_time = time.time()
    sys.stdout.write("""Word asked          : []
Word writen         : []
Was right           : [-]
Time to write       : ---- s
Length              : ---- chars
Chars per second    : ---- cps
Penalty             : + ---- s

""")
    for i in range(len(liste[:])):
        word = liste.pop(0)
        start = time.time()
        pressed, result = run_turn(word, liste)
        stats["cpress"] += pressed
        total = time.time() - start
        stats["totaltime"] += total
        if result != word:
            stats["penality"] += (args.penalty / len(word))
        else:
            stats["correct"] += 1
        clear()
        sys.stdout.write("""Word asked          : {}
Word writen         : {}
Was right           : [{}]
Time to write       : {} s
Length              : {} chars
Chars per second    : {} cps
Penalty             : + {} s

""".format(
                word,
                result,
                "\033[92mO\033[0m" if result == word else "\033[91mX\033[0m",
                total,
                len(word),
                len(word) / total,
                (args.penalty / len(word)) if result != word else 0.0
            )
        )
    
    clear()
    sys.stdout.write("""Words asked                             : {}
Total chars asked (without spaces)      : {}
Total key pressed (without spaces)      : {}
Words answered correctly                : {}
Total penalty loss                      : {}
Total atomic time                       : {}

Total compensed time                    : {}
Average chars per seconds               : {}
""".format(
            stats["wasked"],
            stats["casked"],
            stats["cpress"],
            stats["correct"],
            stats["penality"],
            stats["totaltime"],
            stats["totaltime"] + stats["penality"],
            stats["casked"] / (stats["totaltime"] + stats["penality"])
        )
    )
    sys.stdout.flush()
