import getch
import sys

def get_chr():
    inpt = getch.getch()
    if inpt == '\x7f':
        return -1
    elif inpt in "abcdefghijklmnopqrstuvwxyz-'":
        return inpt
    elif inpt == ' ':
        return 1

    return ''

def build_nexts(nexts):
    colors = [
        "\033[48;2;0;0;0m \033[38;2;77;77;77m{}\033[0m",
        "\033[48;2;0;0;0m \033[38;2;60;60;60m{}\033[0m",
        "\033[48;2;0;0;0m \033[38;2;30;30;30m{}\033[0m",
        "\033[48;2;0;0;0m \033[38;2;17;17;17m{}\033[0m",
        "\033[48;2;0;0;0m \033[38;2;0;0;0m{}\033[0m"
    ]
    final = ''
    for i in range(5):
        if i >= len(nexts):
            break
        final += colors[i].format(nexts[i])
    return final

def plen(string):
    l = 0
    is_in_esc_code = False
    for char in string:
        if char in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r" and not is_in_esc_code:
            l += 1
        if char == "\033":
            is_in_esc_code = True
        if char == 'm':
            is_in_esc_code = False
    return l

def run_turn(target, nexts):
    string = ''
    fnexts = build_nexts(nexts)
    l = plen(target) + plen(fnexts)
    sys.stdout.write(f"\033[48;2;0;0;0m\033[94m{target}{fnexts}\r")
    sys.stdout.flush()
    inpt = None
    while inpt != 1:
        inpt = get_chr()
        if inpt == -1:
            string = string[:-1]
            sys.stdout.write("\b\033[48;2;0;0;0m\033[94m")
            sys.stdout.write(target[len(string)])
            sys.stdout.write("\b")
            sys.stdout.flush()
            continue
        if inpt == 1:
            continue
        if type(inpt) != str:
            raise ValueError(f"Got an unexpected value {inpt} of type {type(inpt)}")

        string += inpt
        if not inpt:
            continue

        sys.stdout.write("\033[48;2;0;0;0m")
        sys.stdout.write("\033[92m" if target.startswith(string) else "\033[91m")
        sys.stdout.write(inpt)
        sys.stdout.flush()
    
    sys.stdout.write("\033[0m" + (' ' * l) + '\r')

    return string == target
        
if __name__ == "__main__":
    x = run_turn("target", ["is", "a", "sample", "phrase", "to", "say", "hello", "world"])