# Write Speed Test

---

## Test your keyboard speed. Type as fast af !

---

### Installation

To use this tool, follow these steps :

- Install python3 (`sudo apt-get install python3` on Debian based linux distributions)
- [OPTIONAL] Setup Python Virtual Environment :
  - Run `python3 -m venv .venv` to create the virtual environment
  - Run `source ./.venv/bin/activate` to activate the virtual environment
- Install dependencies : run `python3 -m pip install -r requirements.txt`
- All done ! Run `./writetest.py` to run !

### Run

To run this script, you will need to parse at least one command line argument :

- -d, --database, which contains all the possible words asked by the program. Some default are available : english.db, french.db and programing.db

The following are optionals arguments :

- -n, --number, which contains the ammount of words asked by the program. Default is 30

- -p, --penalty, represent the amount of seconds you will lose as a penalty, if you miss a word. This vary depending on the length of the missed word : The longer the word is, the less time you will lose. The computation is simple : divide the penalty value by the length of the word, and add this to the final compensed time.

Hope it help,
I know the code is messy and disgusting, do not juge, I was tired