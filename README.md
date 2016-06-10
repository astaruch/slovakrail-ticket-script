# slovakrail-ticket-script
Script for automated buying ticket for slovak rails https://www.slovakrail.sk/sk/internetovy-obchod/internetovy-obchod-zssk.html

Script will click on buttons, and fill up the input boxes for you, from the file `person.txt`. Source code is self-explanatory with comments, so you can edit it, with the proper values (e.g. I am student, if you are not, you need to change it in source).

# Requirements
- python3
- pip packages:
- flake8==2.5.4
- mccabe==0.4.0
- pep8==1.7.0
- pyflakes==1.0.0
- selenium==2.53.2
- Unidecode==0.4.19
- Firefox<47

# Installation
## virtual environment (recommended)
Best way to use it now is making own virtualenv with python3, and then install requirements. For this task, look for [virtualenv] (https://github.com/pypa/virtualenv) or [virtualenvwrapper] (https://pypi.python.org/pypi/virtualenvwrapper).
```
mkvirtualenv zssk
workon zssk
git clone https://github.com/astaruch/slovakrail-ticket-script.git
pip install -r requirements.txt
```

## without virtualenv
You can also run it without virtualenvironment, just download the source file and run with python.

```
git clone https://github.com/astaruch/slovakrail-ticket-script.git
pip install -r requirements.txt
```

# Usage
You need the file `person.txt`. Create new or edit the sample, with info about you.

The execute script with help option for more info:
```
python buy_ticket -h

usage: buy_ticket.py [-h] [--from-city FROM_CITY] [--to-city TO_CITY]
                     [--time TIME] [--name NAME] [--number NUMBER] [--txt TXT]
                     OPTION
```

You need to define, that you want to buy ticket, cities with exact same name like they are on the website and some info about the train.

# Examples
```
    python buy_ticket.py buy -f 'Bratislava hl.st.' -to Kúty -t 04:55
    python buy_ticket.py buy -f Kúty -to 'Bratislava hl.st.' --name Slovan
```

# Video

![Usage](usage.gif?raw=true "Usage")
